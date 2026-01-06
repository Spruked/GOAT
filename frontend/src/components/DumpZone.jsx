import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import CaleonMessage from "./CaleonMessage";

export default function DumpZone({ projectId, onUploadComplete }) {
	const [caleonKey, setCaleonKey] = useState(null);
	const [uploadProgress, setUploadProgress] = useState(0);
	const [fileCount, setFileCount] = useState(0);

	const onDrop = useCallback(async (acceptedFiles) => {
		if (acceptedFiles.length === 0) return;

		setFileCount(acceptedFiles.length);
		setCaleonKey("FIRST_UPLOAD");
		setUploadProgress(0);

		const formData = new FormData();
		acceptedFiles.forEach(file => formData.append("files", file));
		formData.append("projectId", projectId);

		const xhr = new XMLHttpRequest();

		xhr.upload.onprogress = (e) => {
			if (e.lengthComputable) {
				const percent = Math.round((e.loaded / e.total) * 100);
				setUploadProgress(percent);
			}
		};

		xhr.onload = () => {
			if (xhr.status === 200) {
				setCaleonKey("PROCESSING_COMPLETE");
				setTimeout(() => {
					setCaleonKey(null);
					onUploadComplete?.();
				}, 7000);
			}
		};

		xhr.open("POST", "/api/ingest/upload");
		xhr.send(formData);
	}, [projectId, onUploadComplete]);

	const { getRootProps, getInputProps, isDragActive, open } = useDropzone({
		onDrop,
		noClick: false,
		noKeyboard: true,
	});

	return (
		<>
			<div className="min-h-screen flex items-center justify-center px-6 bg-black">
				<div {...getRootProps()} className="w-full max-w-5xl cursor-pointer">
					<input {...getInputProps()} directory="" webkitdirectory="" mozdirectory="" />

					<div className={`relative border-4 border-dashed rounded-3xl p-16 text-center transition-all duration-700
						${isDragActive 
							? "border-cyan-400 bg-cyan-950/40 shadow-2xl shadow-cyan-500/30 scale-105" 
							: "border-cyan-800/40 hover:border-cyan-600/70"}`}>

						{/* Live upload overlay when active */}
						{uploadProgress > 0 && (
							<div className="absolute inset-0 bg-black/90 rounded-3xl flex flex-col items-center justify-center gap-6">
								<div className="w-64 h-3 bg-cyan-950/60 rounded-full overflow-hidden">
									<div 
										className="h-full bg-gradient-to-r from-cyan-500 to-amber-500 transition-all duration-500"
										style={{ width: `${uploadProgress}%` }}
									/>
								</div>
								<p className="text-cyan-100 text-xl">
									{uploadProgress < 100 ? `Uploading ${fileCount} items… ${uploadProgress}%` : "Finalizing…"}
								</p>
							</div>
						)}

						<img 
							src="/caleonia-glow.png" 
							alt="Caleon" 
							className="w-32 h-32 mx-auto mb-10 animate-gpu-float"
						/>

						<h1 className="text-5xl font-light text-cyan-100 mb-6 tracking-wider">
							{isDragActive ? "Release everything here" : "Drop your entire world"}
						</h1>

						<p className="text-cyan-300 text-xl leading-relaxed max-w-2xl mx-auto mb-10">
							Photos • Scanned letters • Voice memos • Blueprints • PDFs • Entire folders • Phone backups
							<br />
							<span className="text-amber-400">Private. Encrypted. Forever yours.</span>
						</p>

						<button
							onClick={open}
							className="px-16 py-6 bg-gradient-to-r from-cyan-600/20 to-amber-600/20 border border-cyan-500 rounded-2xl text-cyan-100 text-2xl hover:from-cyan-600/30 hover:to-amber-600/30 transition-all backdrop-blur"
						>
							Or choose files / folders
						</button>
					</div>
				</div>
			</div>

			<CaleonMessage messageKey={caleonKey} />
		</>
	);
}