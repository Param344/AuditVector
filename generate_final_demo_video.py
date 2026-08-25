import os
import sys
import subprocess
import asyncio
import time
from PIL import Image, ImageDraw, ImageFont
import edge_tts
import imageio_ffmpeg

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()
BASE_DIR = "/Users/paramjeetsingh/Desktop/AuditVector/AuditVector"
SCRATCH_DIR = "/Users/paramjeetsingh/.gemini/antigravity-cli/brain/161fde66-4dec-4965-b6aa-912a394f0c19/scratch"
IMG_DIR = os.path.join(BASE_DIR, "docs", "screenshots")
OUT_VIDEO_DOCS = os.path.join(BASE_DIR, "docs", "AuditVector_Demo_Video.mp4")
OUT_VIDEO_ARTIFACTS = "/Users/paramjeetsingh/.gemini/antigravity-cli/brain/161fde66-4dec-4965-b6aa-912a394f0c19/AuditVector_Demo_Video.mp4"

os.makedirs(SCRATCH_DIR, exist_ok=True)

# 10 Distinct Scenes matching our 10 new high-resolution screenshots
SCENES = [
    {
        "id": 1,
        "image": os.path.join(IMG_DIR, "01_landing_launchpad.png"),
        "top_badge": "AUDITVECTOR • ALL THINGS AGENTIC HACKATHON",
        "caption": "Autonomous Financial Integrity Investigator • 'AI reasons. Code proves. Evidence explains.'",
        "voice_text": "Welcome to AuditVector, an autonomous financial integrity investigation agent built for the All Things Agentic Hackathon. In quantitative finance, subtle software bugs such as inverted returns, double-counted fees, and configuration drift silently misstate millions of dollars in capital. Because large language models cannot solve this with probabilistic guesswork on millions of rows, AuditVector is built on a strict principle: AI reasons, Code proves, and Evidence explains."
    },
    {
        "id": 2,
        "image": os.path.join(IMG_DIR, "02_live_multiagent_stepper.png"),
        "top_badge": "6-AGENT GOOGLE ADK PIPELINE + GEMINI 3.5 FLASH",
        "caption": "Live Asynchronous Multi-Agent Stepper • Adaptive Evidence-Driven Routing Loop",
        "voice_text": "Under the hood, AuditVector orchestrates six specialized Google Agent Development Kit agents powered by Gemini 3.5 Flash with an evidence-driven adaptive loop. When an audit mission begins, our live command center streams real-time telemetry: AuditPlanner scopes the codebase, RepositoryInvestigator maps AST routines, FinancialInvestigator extracts claimed metrics, ContradictionInvestigator executes deterministic reconcilers, RemediationAgent verifies surgical diffs in an isolated sandbox, and ReportAgent synthesizes the final evidence."
    },
    {
        "id": 3,
        "image": os.path.join(IMG_DIR, "03_alpha_verdict_claim_vs_reality.png"),
        "top_badge": "INTEGRITYLAB ALPHA FAILURE BENCHMARK • $44,276.75 DISCREPANCY",
        "caption": "Claimed PnL: +$18,240.00 | Deterministic Ground Truth: -$3,720.00 (Variance: -$21,960.00)",
        "voice_text": "In under a second, AuditVector delivers its forensic verdict on our primary benchmark, IntegrityLab Alpha: over forty-four thousand dollars in capital discrepancy discovered across four verified contradictions, resulting in a Grade F Financial Integrity Score. Look at the Claim versus Reality hero card: while the software claimed a positive eighteen thousand dollar PnL, deterministic reconstruction proves an actual net loss of thirty-seven hundred dollars, uncovering a critical twenty-one thousand nine hundred and sixty dollar capital misstatement."
    },
    {
        "id": 4,
        "image": os.path.join(IMG_DIR, "04_verified_findings_why_traversal.png"),
        "top_badge": "VERIFIED FINDINGS EXPLORER & WHY EVIDENCE TRAVERSAL",
        "caption": "Interactive 4-Step Provenance Traversal • Source Code to Canonical Transaction Fills",
        "voice_text": "In the Verified Findings explorer, auditors can examine each failure in detail, including PnL breakdowns, polarity inversions, fee double-counting, and fee model rate drift. Notice our interactive WHY Evidence Provenance Traversal: it walks the auditor step-by-step through mathematical variance, canonical transaction fills, AST source code citations, and the sealed deterministic verifier contract."
    },
    {
        "id": 5,
        "image": os.path.join(IMG_DIR, "05_autonomous_remediation_sandbox.png"),
        "top_badge": "AUTONOMOUS REMEDIATION & ISOLATED VERIFICATION SANDBOX",
        "caption": "Variance Drops $21,960.00 ➔ $0.00 (RESOLVED) • Zero Repo Modification Without Approval",
        "voice_text": "AuditVector doesn't just find contradictions; it autonomously formulates surgical unified diff remediation patches. Crucially, candidate patches are tested strictly inside an isolated verification sandbox with regression test execution. For this sign inversion bug, sandbox re-verification proves that the post-patch variance drops immediately to zero dollars with one hundred percent passing regression checks, all while requiring human authorization before touching any repository."
    },
    {
        "id": 6,
        "image": os.path.join(IMG_DIR, "06_forensic_evidence_drawer.png"),
        "top_badge": "SEALED CRYPTOGRAPHIC EVIDENCE CONTRACTS",
        "caption": "SHA-256 Dataset Anchors • Line-Level AST Citations • Deterministic Verifier Proof",
        "voice_text": "AuditVector enforces a strict invariant: No Evidence Contract, No Verified Finding. Clicking Inspect Evidence Contract opens our slide-out drawer, revealing exact reported versus reconstructed numbers, mathematical variances, canonical normalizer versions, and cryptographic SHA-256 anchors for tamper-proof risk and compliance archiving."
    },
    {
        "id": 7,
        "image": os.path.join(IMG_DIR, "07_audit_replay_adaptive_decisions.png"),
        "top_badge": "AUDIT MISSION REPLAY & ADAPTIVE DECISION LOG",
        "caption": "Interactive Investigation Scrubber • Real-Time Autonomous ADK Routing Choices",
        "voice_text": "With our seven-stage Audit Replay controller, judges and institutional auditors can step backward and forward through the entire investigation lifecycle. Below the replay scrubber, the ADK Adaptive Routing Decision Log records every autonomous routing choice made by the agents as evidence accumulates."
    },
    {
        "id": 8,
        "image": os.path.join(IMG_DIR, "08_cryptographic_provenance_graph.png"),
        "top_badge": "INTERACTIVE CRYPTOGRAPHIC PROVENANCE GRAPH",
        "caption": "Full Chain of Custody: Source Code ➔ Raw Data ➔ Normalizer ➔ Verifier ➔ Contract",
        "voice_text": "The Interactive Cryptographic Provenance Graph visualizes the complete immutable chain of custody. Auditors can trace from raw trade files through canonical normalization, deterministic verification engines, and final sealed finding contracts, clicking any node to inspect its cryptographic metadata."
    },
    {
        "id": 9,
        "image": os.path.join(IMG_DIR, "09_control_clean_baseline_100_fis.png"),
        "top_badge": "INTEGRITYLAB CONTROL CLEAN BASELINE • ZERO FALSE POSITIVES",
        "caption": "Financial Integrity Score: 100/100 (Grade A+) • Zero Discrepancy • Remediation Bypassed",
        "voice_text": "To prove our agents avoid false positives, we audited IntegrityLab Control, a clean baseline. In moments, the UI confirms one hundred percent financial integrity: a perfect one hundred out of one hundred Financial Integrity Score, Grade A-plus, zero dollar discrepancy, and zero false contradictions. The remediation agent is autonomously bypassed because calculations match deterministic ground truth."
    },
    {
        "id": 10,
        "image": os.path.join(IMG_DIR, "10_aibip_quantitative_dogfood.png"),
        "top_badge": "AI-BIP QUANTITATIVE DOGFOOD • LIVE FIREBASE SHOWCASE",
        "caption": "$16,286.24 Discrepancy Proven (30.0% Profit Erosion) • 63/63 Tests Passing • Live on Firebase",
        "voice_text": "Finally, we dogfooded AuditVector on AI-BIP, a real-world multi-token quantitative momentum strategy. AuditVector uncovered a sixteen thousand two hundred and eighty-six dollar discrepancy, representing a thirty point zero percent erosion of reported profits against actual trade fills. With sixty-three automated tests passing and a live zero-cost showcase on Firebase Hosting, AuditVector sets a new standard for provable, autonomous financial agents. Thank you!"
    }
]

def get_audio_duration(file_path):
    cmd = [
        FFMPEG_BIN, "-i", file_path,
        "-hide_banner"
    ]
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    _, err = p.communicate()
    for line in err.decode("utf-8", errors="ignore").splitlines():
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = parts.split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
    return 15.0

def create_styled_frame(scene, out_path, target_w=1920, target_h=1080):
    img = Image.open(scene["image"]).convert("RGBA")
    
    # Base canvas: Dark forensic theme
    bg = Image.new("RGBA", (target_w, target_h), (11, 15, 25, 255))
    
    # Inner viewport scale for screenshot (center fit)
    max_h = 920
    scale = min((target_w - 40) / img.width, max_h / img.height)
    new_w = int(img.width * scale)
    new_h = int(img.height * scale)
    resized_img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    offset_x = (target_w - new_w) // 2
    offset_y = 65 + (max_h - new_h) // 2
    
    # Paste screenshot
    bg.paste(resized_img, (offset_x, offset_y), resized_img)
    
    # Overlay graphics
    draw = ImageDraw.Draw(bg)
    
    # 1. Top Bar Banner
    draw.rectangle([(0, 0), (target_w, 56)], fill=(15, 23, 42, 240))
    draw.line([(0, 56), (target_w, 56)], fill=(51, 65, 85, 255), width=2)
    
    # 2. Bottom Caption Banner
    draw.rectangle([(0, target_h - 70), (target_w, target_h)], fill=(15, 23, 42, 245))
    draw.line([(0, target_h - 70), (target_w, target_h - 70)], fill=(51, 65, 85, 255), width=2)
    
    # Load fonts
    try:
        font_badge = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
        font_caption = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
        font_brand = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
    except Exception:
        font_badge = ImageFont.load_default()
        font_caption = ImageFont.load_default()
        font_brand = ImageFont.load_default()
    
    # Brand logo left
    draw.text((30, 16), "🛡️ AUDITVECTOR", font=font_brand, fill=(96, 165, 250, 255))
    
    # Scene Top Badge center/right
    draw.text((target_w - 750, 17), scene["top_badge"], font=font_badge, fill=(244, 244, 245, 255))
    
    # Bottom Caption
    draw.text((40, target_h - 48), scene["caption"], font=font_caption, fill=(226, 232, 240, 255))
    
    bg.convert("RGB").save(out_path, "JPEG", quality=95)
    print(f"🖼️ Rendered styled frame for Scene {scene['id']}")

async def generate_voiceover(scene):
    voice_file = os.path.join(SCRATCH_DIR, f"voice_scene_{scene['id']}.mp3")
    communicate = edge_tts.Communicate(scene["voice_text"], "en-US-AndrewNeural", rate="+3%", pitch="+0Hz")
    await communicate.save(voice_file)
    dur = get_audio_duration(voice_file)
    print(f"🎙️ Scene {scene['id']} Audio generated ({dur:.2f}s): '{scene['voice_text'][:50]}...'")
    return voice_file, dur

async def main():
    print("==========================================================")
    print("🎬 GENERATING BROADCAST-QUALITY AUDITVECTOR DEMO VIDEO")
    print("==========================================================")
    
    clip_files = []
    
    for scene in SCENES:
        sid = scene["id"]
        frame_file = os.path.join(SCRATCH_DIR, f"frame_scene_{sid}.jpg")
        clip_file = os.path.join(SCRATCH_DIR, f"clip_scene_{sid}.mp4")
        
        # 1. Create Frame
        create_styled_frame(scene, frame_file)
        
        # 2. Generate Audio Voiceover
        voice_file, duration = await generate_voiceover(scene)
        
        # Pad duration by 0.5s for clean audio pause between scenes
        clip_duration = duration + 0.4
        
        # 3. Create MP4 Video Clip with exact audio synchronization
        cmd = [
            FFMPEG_BIN, "-y",
            "-loop", "1",
            "-i", frame_file,
            "-i", voice_file,
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-pix_fmt", "yuv420p",
            "-r", "30",
            "-t", str(clip_duration),
            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "44100",
            "-af", "apad=pad_dur=0.4",
            "-shortest",
            clip_file
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print(f"❌ FFmpeg error on Scene {sid}: {res.stderr.decode('utf-8')}")
            sys.exit(1)
        
        print(f"✅ Scene {sid} Clip created: {clip_file} (Duration: {clip_duration:.2f}s)")
        clip_files.append(clip_file)

    # 4. Concatenate All 10 Clips into Final Demo Video
    concat_list_file = os.path.join(SCRATCH_DIR, "concat_list.txt")
    with open(concat_list_file, "w") as f:
        for cf in clip_files:
            f.write(f"file '{cf}'\n")

    print("\n🎞️ Concatenating 10 scenes into final video...")
    concat_cmd = [
        FFMPEG_BIN, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_file,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        OUT_VIDEO_DOCS
    ]
    res = subprocess.run(concat_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        print(f"❌ Concat error: {res.stderr.decode('utf-8')}")
        sys.exit(1)

    # Copy to artifacts directory
    subprocess.run(["cp", "-f", OUT_VIDEO_DOCS, OUT_VIDEO_ARTIFACTS])

    final_dur = get_audio_duration(OUT_VIDEO_DOCS)
    file_size_mb = os.path.getsize(OUT_VIDEO_DOCS) / (1024 * 1024)
    print("==========================================================")
    print(f"🎉 FINAL DEMO VIDEO CREATED SUCCESSFULLY!")
    print(f"📁 Path: {OUT_VIDEO_DOCS}")
    print(f"⏱️ Total Duration: {int(final_dur // 60)}m {int(final_dur % 60)}s ({final_dur:.2f}s)")
    print(f"💾 File Size: {file_size_mb:.2f} MB")
    print("==========================================================")

if __name__ == "__main__":
    asyncio.run(main())
