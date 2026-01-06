import { useEffect, useState } from "react";
import caleonDialogue from "../data/caleonDialogue.json";

export default function CaleonMessage({ messageKey, autoHideMs }) {
	const [visible, setVisible] = useState(false);

	useEffect(() => {
		if (!messageKey) return setVisible(false);
		setVisible(true);

		if (autoHideMs) {
			const t = setTimeout(() => setVisible(false), autoHideMs);
			return () => clearTimeout(t);
		}
	}, [messageKey, autoHideMs]);

	if (!visible || !messageKey) return null;

	return (
		<div className="fixed inset-x-0 bottom-8 z-50 flex justify-center pointer-events-none">
			<div className="w-full max-w-3xl px-6">
				{/* GPU-accelerated card */}
				<div className="relative isolate overflow-hidden rounded-2xl bg-black/80 backdrop-blur-xl border border-cyan-800/30 shadow-2xl
												will-change-transform translate-z-0">
          
					{/* Ultra-light breathing glow (only opacity) */}
					<div className="absolute inset-0 bg-cyan-500/10 animate-gpu-pulse" />

					<div className="relative flex items-start gap-6 p-6">
						{/* Avatar container – forces its own GPU layer */}
						<div className="relative flex-shrink-0 will-change-transform translate-z-0">
							{/* Particle sparks behind her head */}
							<div className="absolute inset-0 -z-10 pointer-events-none">
								{Array.from({ length: 8 }).map((_, i) => (
									<div
										key={i}
										className="absolute w-1 h-1 rounded-full bg-cyan-300/60 animate-particle"
										style={{
											left: `${20 + Math.random() * 60}%`,
											top: `${20 + Math.random() * 60}%`,
											animationDelay: `${i * 1.7}s`,
										}}
									></div>
								))}
							</div>
							<div className="w-24 h-24 rounded-full overflow-hidden border-2 border-cyan-600/50 shadow-xl">
								<img
									src="/caleonblue.jpg"
									alt="Caleon"
									className="h-full w-full object-cover animate-gpu-float"
									loading="eager"
								/>
								{/* Eye glow – only opacity */}
								<div className="absolute inset-0 rounded-full bg-amber-400/40 animate-gpu-eye" />
							</div>

							{/* Single ping ring – one element only */}
							<div className="absolute -inset-1 rounded-full border border-cyan-400/40 animate-gpu-ping" />
						</div>

						{/* Text – no layout shifts */}
						<p className="text-cyan-100 text-lg leading-relaxed font-light pt-2">
							{caleonDialogue[messageKey]}
						</p>
					</div>
				</div>
			</div>
		</div>
	);
}