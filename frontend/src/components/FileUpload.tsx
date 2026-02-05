"use client";

import { useState } from "react";
import { Upload, X, FileVideo, FileImage, CheckCircle, AlertTriangle, Loader2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

export default function FileUpload() {
    const [file, setFile] = useState<File | null>(null);
    const [isDragging, setIsDragging] = useState(false);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [result, setResult] = useState<{ score: number; isReal: boolean; hash: string } | null>(null);

    const handleDrag = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setIsDragging(true);
        } else if (e.type === "dragleave") {
            setIsDragging(false);
        }
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            setFile(e.dataTransfer.files[0]);
            setResult(null);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
            setResult(null);
        }
    };

    const handleAnalyze = async () => {
        if (!file) return;
        setIsAnalyzing(true);

        // Simulate AI processing
        await new Promise(resolve => setTimeout(resolve, 3000));

        // Mock result - alternating for demo
        const isFake = Math.random() > 0.5;
        setResult({
            score: isFake ? 98.2 : 99.1,
            isReal: !isFake,
            hash: "0x7f83...3a91"
        });
        setIsAnalyzing(false);
    };

    return (
        <div id="upload" className="w-full max-w-2xl mx-auto p-6 bg-zinc-900/50 backdrop-blur-md rounded-2xl border border-white/10 shadow-2xl">
            <h2 className="text-2xl font-bold mb-6 text-center">Upload Media for Inspection</h2>

            <div
                className={cn(
                    "relative flex flex-col items-center justify-center w-full h-64 rounded-xl border-2 border-dashed transition-all cursor-pointer overflow-hidden",
                    isDragging ? "border-purple-500 bg-purple-500/10" : "border-zinc-700 bg-zinc-900/50 hover:bg-zinc-800",
                    file ? "border-purple-500/50" : ""
                )}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => document.getElementById("file-upload")?.click()}
            >
                <input
                    id="file-upload"
                    type="file"
                    className="hidden"
                    onChange={handleChange}
                    accept="image/*,video/*"
                />

                <AnimatePresence mode="wait">
                    {file ? (
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.9 }}
                            className="flex flex-col items-center gap-4"
                        >
                            {file.type.startsWith('video') ? (
                                <FileVideo className="w-16 h-16 text-purple-400" />
                            ) : (
                                <FileImage className="w-16 h-16 text-purple-400" />
                            )}
                            <div className="text-center">
                                <p className="font-medium text-lg">{file.name}</p>
                                <p className="text-sm text-zinc-400">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                            </div>
                            <button
                                onClick={(e) => { e.stopPropagation(); setFile(null); setResult(null); }}
                                className="absolute top-4 right-4 p-1 hover:bg-zinc-700 rounded-full"
                            >
                                <X className="w-5 h-5 text-zinc-400" />
                            </button>
                        </motion.div>
                    ) : (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="flex flex-col items-center gap-4 text-zinc-400"
                        >
                            <Upload className="w-12 h-12 mb-2" />
                            <p className="text-lg font-medium">Drag & drop or click to upload</p>
                            <p className="text-sm text-zinc-500">Supports MP4, AVI, JPG, PNG</p>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>

            {/* Action Button */}
            <div className="mt-6 flex justify-center">
                <button
                    onClick={handleAnalyze}
                    disabled={!file || isAnalyzing}
                    className="w-full sm:w-auto px-8 py-3 bg-white text-black font-bold rounded-full disabled:opacity-50 disabled:cursor-not-allowed hover:bg-zinc-200 transition-colors flex items-center justify-center gap-2 cursor-pointer"
                >
                    {isAnalyzing ? (
                        <>
                            <Loader2 className="w-5 h-5 animate-spin" />
                            Analyzing via AI Grid...
                        </>
                    ) : (
                        "Verify Authenticity"
                    )}
                </button>
            </div>

            {/* Results */}
            <AnimatePresence>
                {result && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="mt-8 p-6 rounded-xl bg-black border border-white/10"
                    >
                        <div className="flex items-center justify-between mb-4">
                            <span className="text-sm text-zinc-400">Analysis Result</span>
                            <span className="text-xs font-mono text-zinc-600">{result.hash}</span>
                        </div>

                        <div className="flex items-center gap-4 mb-6">
                            {result.isReal ? (
                                <div className="p-3 rounded-full bg-green-500/20 text-green-500">
                                    <CheckCircle className="w-8 h-8" />
                                </div>
                            ) : (
                                <div className="p-3 rounded-full bg-red-500/20 text-red-500">
                                    <AlertTriangle className="w-8 h-8" />
                                </div>
                            )}
                            <div>
                                <h3 className="text-2xl font-bold">{result.isReal ? "Authentic Media" : "Deepfake Detected"}</h3>
                                <p className="text-zinc-400">Confidence Score: <span className={result.isReal ? "text-green-400" : "text-red-400"}>{result.score}%</span></p>
                            </div>
                        </div>

                        <div className="w-full bg-zinc-800 rounded-full h-2 overflow-hidden">
                            <div
                                className={cn("h-full transition-all duration-1000", result.isReal ? "bg-green-500" : "bg-red-500")}
                                style={{ width: `${result.score}%` }}
                            />
                        </div>

                        <div className="mt-4 pt-4 border-t border-white/10 text-center">
                            <p className="text-xs text-zinc-500 uppercase tracking-widest mb-2">Blockchain Proof</p>
                            <a href="#" className="text-purple-400 hover:text-purple-300 text-sm font-mono underline decoration-dotted">
                                View Transaction on PolygonScan
                            </a>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
