import { ArrowRight, ShieldCheck, Upload } from "lucide-react";
import Link from "next/link";
import FileUpload from "@/components/FileUpload";

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white selection:bg-purple-500/30">
      {/* Navbar */}
      <nav className="fixed top-0 w-full z-50 border-b border-white/10 bg-black/50 backdrop-blur-xl">
        <div className="container mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-6 h-6 text-purple-500" />
            <span className="font-bold text-lg tracking-tight">DeepTrust</span>
          </div>
          <div className="hidden md:flex gap-8 text-sm font-medium text-zinc-400">
            <Link href="#" className="hover:text-white transition-colors">How it works</Link>
            <Link href="#" className="hover:text-white transition-colors">Technology</Link>
            <Link href="#" className="hover:text-white transition-colors">Blockchain</Link>
          </div>
          <button className="bg-white text-black px-4 py-2 rounded-full text-sm font-bold hover:bg-zinc-200 transition-colors cursor-pointer">
            Connect Wallet
          </button>
        </div>
      </nav>

      {/* Hero */}
      <main className="flex flex-col items-center justify-center pt-32 pb-20 px-4 text-center relative overflow-hidden">
        {/* Background Effects */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[500px] bg-purple-600/20 opacity-30 blur-[100px] rounded-full -z-10"></div>

        <div className="space-y-6 max-w-4xl mx-auto z-10 mb-20">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-white/10 bg-white/5 text-sm text-purple-400 mb-6">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-purple-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-purple-500"></span>
            </span>
            Live on Polygon Testnet
          </div>

          <h1 className="text-5xl md:text-7xl font-bold tracking-tight bg-gradient-to-b from-white via-white to-white/60 bg-clip-text text-transparent pb-2">
            Verify Reality in the <br /> Digital Age
          </h1>

          <p className="text-lg md:text-xl text-zinc-400 max-w-2xl mx-auto leading-relaxed">
            The world's first decentralized deepfake detection protocol.
            Powered by advanced AI and secured by the immutable blockchain.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-8">
            <Link href="#upload" className="group flex items-center gap-2 bg-purple-600 hover:bg-purple-500 text-white px-8 py-4 rounded-full text-lg font-semibold transition-all hover:scale-105 shadow-[0_0_40px_-10px_rgba(147,51,234,0.5)] cursor-pointer">
              <Upload className="w-5 h-5" />
              Analyze Media
            </Link>
            <button className="group flex items-center gap-2 text-zinc-400 hover:text-white px-8 py-4 rounded-full text-lg font-medium transition-colors cursor-pointer">
              View Smart Contract <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </button>
          </div>
        </div>

        {/* Analysis Section */}
        <div className="w-full max-w-4xl mx-auto">
          <FileUpload />
        </div>
      </main>
    </div>
  );
}
