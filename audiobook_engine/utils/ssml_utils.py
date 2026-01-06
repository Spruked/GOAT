# audiobook_engine/utils/ssml_utils.py
"""
SSML Utilities for Audiobook Engine

Helper functions for SSML processing and manipulation.
"""

import re
import logging
from typing import List, Optional, Dict, Any, Tuple
from xml.etree import ElementTree as ET

# Configure logging
logger = logging.getLogger(__name__)


def clean_ssml_text(text: str) -> str:
    """
    Clean and normalize text for SSML processing.

    Args:
        text: Raw text to clean

    Returns:
        Cleaned text suitable for SSML
    """
    if not text:
        return ""

    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text.strip())

    # Fix common punctuation issues
    text = re.sub(r'\s+([,.!?;:])', r'\1', text)  # Remove space before punctuation
    text = re.sub(r'([,.!?;:])(?=[a-zA-Z])', r'\1 ', text)  # Add space after punctuation

    # Handle quotes
    text = re.sub(r'"\s+', '"', text)  # Remove space after opening quote
    text = re.sub(r'\s+"', '"', text)  # Remove space before closing quote

    return text.strip()


def validate_ssml(ssml_text: str) -> Tuple[bool, Optional[str]]:
    """
    Validate SSML markup for correctness.

    Args:
        ssml_text: SSML text to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Parse XML
        root = ET.fromstring(ssml_text)

        # Check root element
        if root.tag != 'speak':
            return False, "Root element must be 'speak'"

        # Check namespace
        if not root.tag.startswith('{http://www.w3.org/2001/10/synthesis}'):
            logger.warning("SSML should use standard namespace")

        # Basic structure validation
        if not list(root):
            return False, "SSML must contain content"

        return True, None

    except ET.ParseError as e:
        return False, f"XML parsing error: {str(e)}"
    except Exception as e:
        return False, f"Validation error: {str(e)}"


def extract_text_from_ssml(ssml_text: str) -> str:
    """
    Extract plain text from SSML markup.

    Args:
        ssml_text: SSML text

    Returns:
        Plain text content
    """
    try:
        # Parse XML
        root = ET.fromstring(ssml_text)

        # Extract text from all elements
        text_parts = []

        def extract_text(element):
            if element.text:
                text_parts.append(element.text)
            for child in element:
                extract_text(child)
                if child.tail:
                    text_parts.append(child.tail)

        extract_text(root)

        # Join and clean text
        plain_text = ''.join(text_parts)
        return clean_ssml_text(plain_text)

    except Exception as e:
        logger.error(f"Failed to extract text from SSML: {e}")
        return ""


def merge_ssml_segments(ssml_segments: List[str]) -> str:
    """
    Merge multiple SSML segments into a single valid SSML document.

    Args:
        ssml_segments: List of SSML segment strings

    Returns:
        Merged SSML document
    """
    if not ssml_segments:
        return '<?xml version="1.0"?><speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"></speak>'

    try:
        # Parse all segments
        roots = []
        for segment in ssml_segments:
            if segment.strip():
                root = ET.fromstring(segment)
                roots.append(root)

        if not roots:
            return '<?xml version="1.0"?><speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"></speak>'

        # Create new root
        merged_root = ET.Element("speak", {
            "version": "1.0",
            "xmlns": "http://www.w3.org/2001/10/synthesis"
        })

        # Merge content from all roots
        for root in roots:
            for child in list(root):
                merged_root.append(child)

        # Convert back to string
        ssml_str = '<?xml version="1.0"?>'
        ssml_str += ET.tostring(merged_root, encoding='unicode')

        return ssml_str

    except Exception as e:
        logger.error(f"Failed to merge SSML segments: {e}")
        return '<?xml version="1.0"?><speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis">Error merging segments</speak>'


def split_ssml_by_sentences(ssml_text: str, max_length: int = 1000) -> List[str]:
    """
    Split SSML into segments by sentence boundaries.

    Args:
        ssml_text: SSML text to split
        max_length: Maximum character length per segment

    Returns:
        List of SSML segments
    """
    try:
        # Extract plain text to find sentence boundaries
        plain_text = extract_text_from_ssml(ssml_text)

        # Find sentence boundaries in plain text
        sentence_pattern = r'(?<=[.!?])\s+'
        sentences = re.split(sentence_pattern, plain_text)

        # If text is short, return as single segment
        if len(plain_text) <= max_length:
            return [ssml_text]

        # For now, return the original SSML
        # A more sophisticated implementation would map sentence boundaries back to SSML
        logger.warning("SSML sentence splitting not fully implemented, returning original")
        return [ssml_text]

    except Exception as e:
        logger.error(f"Failed to split SSML by sentences: {e}")
        return [ssml_text]


def get_ssml_duration_estimate(ssml_text: str, words_per_minute: int = 150) -> float:
    """
    Estimate duration of SSML content in seconds.

    Args:
        ssml_text: SSML text
        words_per_minute: Speaking rate

    Returns:
        Estimated duration in seconds
    """
    try:
        plain_text = extract_text_from_ssml(ssml_text)

        # Count words
        words = len(plain_text.split())

        # Calculate duration
        minutes = words / words_per_minute
        return minutes * 60

    except Exception as e:
        logger.error(f"Failed to estimate SSML duration: {e}")
        return 0.0


def add_ssml_prosody(ssml_text: str, rate: float = 1.0, pitch: float = 0.0, volume: float = 0.0) -> str:
    """
    Add prosody markup to SSML text.

    Args:
        ssml_text: Input SSML
        rate: Speech rate multiplier (0.5 to 2.0)
        pitch: Pitch adjustment in semitones (-10 to +10)
        volume: Volume adjustment in dB (-6 to +6)

    Returns:
        SSML with prosody markup
    """
    try:
        root = ET.fromstring(ssml_text)

        # Create prosody attributes
        prosody_attrs = {}
        if rate != 1.0:
            prosody_attrs['rate'] = f"{rate}"
        if pitch != 0.0:
            prosody_attrs['pitch'] = f"{pitch}st"
        if volume != 0.0:
            prosody_attrs['volume'] = f"{volume}dB"

        if prosody_attrs:
            # Wrap content in prosody element
            prosody_elem = ET.Element("prosody", prosody_attrs)

            # Move all children to prosody element
            for child in list(root):
                root.remove(child)
                prosody_elem.append(child)

            root.append(prosody_elem)

        return '<?xml version="1.0"?>' + ET.tostring(root, encoding='unicode')

    except Exception as e:
        logger.error(f"Failed to add prosody to SSML: {e}")
        return ssml_text


def extract_ssml_metadata(ssml_text: str) -> Dict[str, Any]:
    """
    Extract metadata from SSML markup.

    Args:
        ssml_text: SSML text

    Returns:
        Dictionary of metadata
    """
    metadata = {
        'has_prosody': False,
        'has_voice': False,
        'has_emotion': False,
        'voice_names': [],
        'estimated_duration': 0.0,
        'word_count': 0
    }

    try:
        root = ET.fromstring(ssml_text)

        # Check for prosody
        for elem in root.iter():
            if elem.tag == 'prosody':
                metadata['has_prosody'] = True
            elif elem.tag == 'voice':
                metadata['has_voice'] = True
                if 'name' in elem.attrib:
                    metadata['voice_names'].append(elem.attrib['name'])
            elif elem.tag.endswith('voice') and 'emotion' in elem.attrib:
                metadata['has_emotion'] = True

        # Get text statistics
        plain_text = extract_text_from_ssml(ssml_text)
        metadata['word_count'] = len(plain_text.split())
        metadata['estimated_duration'] = get_ssml_duration_estimate(ssml_text)

    except Exception as e:
        logger.error(f"Failed to extract SSML metadata: {e}")

    return metadata


def optimize_ssml(ssml_text: str) -> str:
    """
    Optimize SSML for better TTS processing.

    Args:
        ssml_text: Input SSML

    Returns:
        Optimized SSML
    """
    try:
        # For now, just validate and return
        # Future optimizations could include:
        # - Removing redundant markup
        # - Consolidating adjacent elements
        # - Optimizing prosody settings

        is_valid, error = validate_ssml(ssml_text)
        if not is_valid:
            logger.warning(f"SSML optimization skipped due to validation error: {error}")
            return ssml_text

        return ssml_text

    except Exception as e:
        logger.error(f"Failed to optimize SSML: {e}")
        return ssml_text