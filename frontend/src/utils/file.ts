export const formatBytes = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + " " + sizes[i];
};

export const statusColors = {
  processed: "bg-green-600",
  processing: "bg-blue-500",
  uploaded: "bg-yellow-500",
  failed: "bg-red-500",
};

export const getFileIcon = (type: string) => {
  // This will be imported from lucide-react in the component
  // For now, return a string identifier
  if (type?.includes("image")) return "Image";
  if (type?.includes("pdf")) return "FileText";
  if (type?.includes("video")) return "Film";
  return "File";
};

export const getFileTypeFromMime = (mimeType: string): string => {
  if (!mimeType) return "file";
  if (mimeType.startsWith("image/")) return "image";
  if (mimeType.startsWith("video/")) return "video";
  if (mimeType === "application/pdf") return "pdf";
  if (mimeType.includes("document") || mimeType.includes("word")) return "document";
  return "file";
};