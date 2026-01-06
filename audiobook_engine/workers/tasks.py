# audiobook_engine/workers/tasks.py
"""
Task Queue Management for Audiobook Engine

Manages background task queues for audio processing using RQ or Celery.
Provides queue monitoring and worker management.
"""

import os
import logging
import time
from typing import Optional, Dict, Any, Callable
from queue import Queue
from threading import Thread, Event
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logger = logging.getLogger(__name__)


class TaskQueue:
    """Simple in-memory task queue for background processing."""

    def __init__(self, name: str, max_workers: int = 2):
        self.name = name
        self.max_workers = max_workers
        self.queue = Queue()
        self.executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix=f"{name}_worker")
        self.stop_event = Event()
        self.worker_thread: Optional[Thread] = None
        self.is_running = False

    def enqueue(self, func: Callable, *args, **kwargs):
        """Add a task to the queue."""
        self.queue.put((func, args, kwargs))
        logger.debug(f"Task enqueued in {self.name}: {func.__name__}")

    def start(self):
        """Start the task processor."""
        if self.is_running:
            return

        self.is_running = True
        self.stop_event.clear()
        self.worker_thread = Thread(target=self._process_queue, name=f"{self.name}_processor")
        self.worker_thread.daemon = True
        self.worker_thread.start()

        logger.info(f"Task queue {self.name} started with {self.max_workers} workers")

    def stop(self):
        """Stop the task processor."""
        if not self.is_running:
            return

        self.is_running = False
        self.stop_event.set()

        # Wait for current tasks to complete
        self.executor.shutdown(wait=True)

        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=5.0)

        logger.info(f"Task queue {self.name} stopped")

    def _process_queue(self):
        """Process tasks from the queue."""
        while not self.stop_event.is_set():
            try:
                # Get task with timeout
                task = self.queue.get(timeout=1.0)
                func, args, kwargs = task

                # Submit to executor
                future = self.executor.submit(func, *args, **kwargs)

                # Mark task as done
                self.queue.task_done()

                logger.debug(f"Task submitted to {self.name}: {func.__name__}")

            except self.queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error processing task in {self.name}: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """Get queue statistics."""
        return {
            'queue_name': self.name,
            'is_running': self.is_running,
            'queue_size': self.queue.qsize(),
            'max_workers': self.max_workers,
            'active_threads': len(self.executor._threads) if hasattr(self.executor, '_threads') else 0
        }


# Global task queues
audio_processing_queue = TaskQueue("audio_processing", max_workers=2)
project_processing_queue = TaskQueue("project_processing", max_workers=1)


def start_worker(queue_name: str = "all"):
    """Start task queue workers."""
    if queue_name in ("all", "audio"):
        audio_processing_queue.start()

    if queue_name in ("all", "project"):
        project_processing_queue.start()

    logger.info(f"Workers started for: {queue_name}")


def stop_worker(queue_name: str = "all"):
    """Stop task queue workers."""
    if queue_name in ("all", "audio"):
        audio_processing_queue.stop()

    if queue_name in ("all", "project"):
        project_processing_queue.stop()

    logger.info(f"Workers stopped for: {queue_name}")


def enqueue_audio_task(func: Callable, *args, **kwargs):
    """Enqueue a task for audio processing."""
    audio_processing_queue.enqueue(func, *args, **kwargs)


def enqueue_project_task(func: Callable, *args, **kwargs):
    """Enqueue a task for project processing."""
    project_processing_queue.enqueue(func, *args, **kwargs)


def get_queue_stats() -> Dict[str, Any]:
    """Get statistics for all queues."""
    return {
        'audio_processing': audio_processing_queue.get_stats(),
        'project_processing': project_processing_queue.get_stats()
    }


# RQ/Celery integration (optional)
try:
    from redis import Redis
    from rq import Queue as RQQueue
    from rq.job import Job

    # RQ queue instances
    redis_conn = Redis()
    rq_audio_queue = RQQueue('audio_processing', connection=redis_conn)
    rq_project_queue = RQQueue('project_processing', connection=redis_conn)

    def enqueue_rq_task(queue_name: str, func: Callable, *args, **kwargs):
        """Enqueue task using RQ."""
        if queue_name == 'audio':
            queue = rq_audio_queue
        elif queue_name == 'project':
            queue = rq_project_queue
        else:
            raise ValueError(f"Unknown queue: {queue_name}")

        job = queue.enqueue(func, *args, **kwargs)
        logger.info(f"RQ task enqueued: {job.id}")
        return job

    def get_rq_queue_stats() -> Dict[str, Any]:
        """Get RQ queue statistics."""
        return {
            'audio_processing': {
                'queued': rq_audio_queue.count,
                'failed': rq_audio_queue.failed_job_registry.count
            },
            'project_processing': {
                'queued': rq_project_queue.count,
                'failed': rq_project_queue.failed_job_registry.count
            }
        }

    HAS_RQ = True

except ImportError:
    HAS_RQ = False
    logger.info("RQ not available, using in-memory queues")


try:
    from celery import Celery

    # Celery app
    celery_app = Celery('audiobook_engine')
    celery_app.config_from_object('audiobook_engine.config.celery_config')

    def enqueue_celery_task(task_name: str, *args, **kwargs):
        """Enqueue task using Celery."""
        result = celery_app.send_task(task_name, args=args, kwargs=kwargs)
        logger.info(f"Celery task enqueued: {result.id}")
        return result

    HAS_CELERY = True

except ImportError:
    HAS_CELERY = False
    logger.info("Celery not available, using in-memory queues")


# Convenience functions for task submission
def submit_audio_processing_task(func: Callable, *args, **kwargs):
    """Submit audio processing task using best available queue."""
    if HAS_RQ:
        return enqueue_rq_task('audio', func, *args, **kwargs)
    elif HAS_CELERY:
        return enqueue_celery_task('process_audio', *args, **kwargs)
    else:
        return enqueue_audio_task(func, *args, **kwargs)


def submit_project_processing_task(func: Callable, *args, **kwargs):
    """Submit project processing task using best available queue."""
    if HAS_RQ:
        return enqueue_rq_task('project', func, *args, **kwargs)
    elif HAS_CELERY:
        return enqueue_celery_task('process_project', *args, **kwargs)
    else:
        return enqueue_project_task(func, *args, **kwargs)


# Monitoring functions
def monitor_queues(interval_seconds: int = 60):
    """Monitor queue status and log statistics."""
    while True:
        try:
            stats = get_queue_stats()

            if HAS_RQ:
                rq_stats = get_rq_queue_stats()
                stats.update(rq_stats)

            logger.info(f"Queue stats: {stats}")

            time.sleep(interval_seconds)

        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.error(f"Queue monitoring error: {e}")
            time.sleep(interval_seconds)


def cleanup_failed_tasks():
    """Clean up failed tasks from queues."""
    try:
        if HAS_RQ:
            # Clean up RQ failed jobs older than 7 days
            from rq.job import Job
            from datetime import datetime, timedelta

            cutoff = datetime.now() - timedelta(days=7)

            for queue in [rq_audio_queue, rq_project_queue]:
                failed_jobs = queue.failed_job_registry.get_job_ids()
                for job_id in failed_jobs:
                    try:
                        job = Job.fetch(job_id, connection=redis_conn)
                        if job.failed_at and job.failed_at < cutoff:
                            queue.failed_job_registry.remove(job_id)
                            job.delete()
                            logger.info(f"Cleaned up old failed job: {job_id}")
                    except Exception as e:
                        logger.warning(f"Failed to cleanup job {job_id}: {e}")

        logger.info("Failed task cleanup completed")

    except Exception as e:
        logger.error(f"Failed task cleanup error: {e}")


# Initialization
def initialize_workers():
    """Initialize and start all workers."""
    start_worker("all")

    # Start monitoring thread
    monitor_thread = Thread(target=monitor_queues, daemon=True, name="queue_monitor")
    monitor_thread.start()

    logger.info("Audiobook engine workers initialized")


def shutdown_workers():
    """Shutdown all workers gracefully."""
    stop_worker("all")
    logger.info("Audiobook engine workers shutdown")