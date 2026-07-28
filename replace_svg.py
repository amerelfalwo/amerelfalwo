import os

replacements = {
    "Arif Hasan": "Amir Elrefai",
    "Full-Stack Developer": "AI Engineer &amp; CV Expert",
    "Sylhet, Bangladesh": "Mansoura, Egypt",
    "BSc in CSE": "CS Student, Mansoura Univ",
    "Building + Learning + Shipping": "Healthcare AI Innovator",
    "VS Code, Git, Android Studio, Figma": "Python, PyTorch, TF, OpenCV",
    "Dart, C++, Python": "Python, C++, SQL",
    "Flutter": "PyTorch",
    "Node.js": "FastAPI",
    "Firebase, MongoDB": "Postgres, MongoDB",
    "Vercel, Docker, Git": "Docker, Git, Linux",
    "arifhasan.connect@gmail.com - % ./profile.sh --live": "amer003100@gmail.com - % ./profile.sh --live",
    "arifhasan.connect@gmail.com": "amer003100@gmail.com",
    "arif-hasan-672249358": "amir-elfalw-b3a3212b8",
    "@arifhaxn": "@amerelfalwo",
    "@arifhaxnn": "@amerelfalwo",
    "coming soon": "amerelfalwo.github.io"
}

for filename in ["dark.svg", "light.svg"]:
    in_path = f"/tmp/arifhaxn/{filename}"
    out_path = f"/mnt/work/git_portolio/{filename}"
    
    if os.path.exists(in_path):
        with open(in_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        for old_txt, new_txt in replacements.items():
            content = content.replace(f">{old_txt}<", f">{new_txt}<")
            content = content.replace(f"> {old_txt}<", f"> {new_txt}<")
            content = content.replace(old_txt, new_txt)
            
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
            
print("Replaced and generated SVGs.")
