<p align="center">
  <img src="./assets/banner.webp" alt="Dea — Little chaos in a quiet mind." width="100%" />
</p>

<p align="center">
  <samp>COMPUTER ENGINEERING · ÓBUDA UNIVERSITY · BIOTECH RESEARCH LAB · BUDAPEST</samp><br />
  <samp><a href="https://www.linkedin.com/in/nagy-istv%C3%A1n-bence-54b2681b0/">LINKEDIN ↗</a> · <a href="https://deawebdesign.netlify.app/">PORTFOLIO ↗</a></samp>
</p>

<img src="./assets/divider.svg" width="100%" alt="" />

### <samp>01 — WHAT I BUILD</samp>

Research software, mostly. I write the tools that sit between a person in a VR headset
and the data a lab can actually publish: acquisition, sync, robotics bridges, analysis.
On the side I build the things I wish existed for free.

I like offline-first systems, strict contracts between processes, and taking a problem
apart before reaching for a solution.

### <samp>02 — SELECTED WORK</samp>

<table>
  <tr>
    <td><samp>01</samp></td>
    <td><b>VRTelemetry</b> <sub><samp>· PRIVATE</samp></sub><br /><sub><samp>PYTHON · TYPESCRIPT · ELECTRON</samp></sub></td>
    <td>A research instrument for VR studies. Records eye tracking, pose, physiology and hardware state to Parquet at headset rate, scores SSQ / NASA-TLX, and syncs to a central hub — queueing locally when the lab network is gone. Extended through out-of-process plugins for BLE biosensors, medical analytics and a ROS 2 / Unity bridge.</td>
  </tr>
  <tr>
    <td><samp>02</samp></td>
    <td><b>vr-robot-bridge</b> <sub><samp>· PRIVATE</samp></sub><br /><sub><samp>C# · PYTHON · ROS · UNITY</samp></sub></td>
    <td>Streams live HMD and controller poses into a Gazebo / MoveIt robot hand and mirrors it in a Unity XR scene. OpenXR → REP-103 → Unity coordinate conversion, verified by tests; ROS runs in WSL2.</td>
  </tr>
  <tr>
    <td><samp>03</samp></td>
    <td><a href="https://github.com/Deatron01/Project-Mimir"><b>Project-Mimir</b></a><br /><sub><samp>FASTAPI · NODE · POSTGRES · RAG</samp></sub></td>
    <td>Microservices that turn PDFs and DOCX files into exam questions. Semantic chunking, RAG over a vector store, JSON-schema guards against hallucination, a <code>SKIP LOCKED</code> worker pool, and hand-built Moodle XML / PDF export.</td>
  </tr>
  <tr>
    <td><samp>04</samp></td>
    <td><a href="https://github.com/Deatron01/AIWorkGroup"><b>AIWorkGroup</b></a><br /><sub><samp>PYTHON · DOCKER · OLLAMA</samp></sub></td>
    <td>A fully local multi-agent software foundry. Boss, designer, worker, tester and integrator agents coordinate over an event bus with a DAG tracker, human-in-the-loop checkpoints and a live dashboard — all on local models.</td>
  </tr>
  <tr>
    <td><samp>05</samp></td>
    <td><a href="https://github.com/Deatron01/OpenRaConverterModul"><b>OpenRaConverterModul</b></a><br /><sub><samp>C# · ASP.NET CORE · DOCKER</samp></sub></td>
    <td>Code synthesis for the OpenRA RTS engine: an API that turns unit, weapon and trait definitions into decision trees and generates the matching C# trait classes and YAML rules. Part of the OE_Lagrange project, alongside an <a href="https://github.com/Deatron01/OE_Lagrange_Side_Projects">entity-creator service, SQL schemas and a PowerShell environment manager</a>.</td>
  </tr>
  <tr>
    <td><samp>06</samp></td>
    <td><a href="https://github.com/Deatron01/FreeTex"><b>FreeTex</b></a><br /><sub><samp>JAVASCRIPT · CODEMIRROR 6 · ELECTRON</samp></sub></td>
    <td>An Overleaf-style LaTeX editor that runs in the browser or as a desktop app with its own compile server. Local-first projects, BibTeX-aware autocompletion, zip import / export.</td>
  </tr>
  <tr>
    <td><samp>07</samp></td>
    <td><a href="https://github.com/Deatron01/Photoshop"><b>Photoshop</b></a><br /><sub><samp>C# · .NET 8 · WPF</samp></sub></td>
    <td>An image editor for an image-processing course: filters and analytics split into separate core and analytics libraries behind an MVVM WPF front end.</td>
  </tr>
  <tr>
    <td><samp>08</samp></td>
    <td><a href="https://github.com/Deatron01/ZizgoKereso"><b>ZizgoKereso</b></a><br /><sub><samp>PYTHON · OPENCV · PYQT6 · C# · BLENDER</samp></sub></td>
    <td>"Where's Zizgő?" — finds a figure in a busy photo. Blender renders the reference set across camera angles and lighting, then HSV colour-masked template matching locates the best hit, with a live heatmap view. Built twice: PyQt6 + OpenCV and C# WinForms.</td>
  </tr>
  <tr>
    <td><samp>09</samp></td>
    <td><a href="https://github.com/Deatron01/AdBlocker"><b>AdBlocker</b></a><br /><sub><samp>JAVASCRIPT · MANIFEST V3</samp></sub></td>
    <td>A Chrome extension on <code>declarativeNetRequest</code> with popup and redirect guards and on-the-fly domain learning. Collects nothing.</td>
  </tr>
  <tr>
    <td><samp>10</samp></td>
    <td><a href="https://github.com/Deatron01/PhoneMirror"><b>PhoneMirror</b></a><br /><sub><samp>PYTHON · WEB</samp></sub></td>
    <td>Free, self-hosted phone mirroring that works on any device.</td>
  </tr>
</table>

<details>
<summary><samp>MORE — SMALLER PROJECTS &amp; COURSEWORK</samp></summary>
<br />
<table>
  <tr><td><a href="https://github.com/Deatron01/Gen_AI_DP3HYC">Gen_AI_DP3HYC</a></td><td><sub><samp>PYTORCH LIGHTNING</samp></sub></td><td>A DCGAN that learns to generate flower images.</td></tr>
  <tr><td><a href="https://github.com/Deatron01/Szakszigo-Gyakorlo">Szakszigo-Gyakorlo</a></td><td><sub><samp>C#</samp></sub></td><td>Every classic programming theorem implemented and commented, for exam practice.</td></tr>
  <tr><td><a href="https://github.com/Deatron01/Erika-konyhaja">Erika-konyhaja</a></td><td><sub><samp>VITE · TAILWIND</samp></sub></td><td>A live website for a small kitchen business.</td></tr>
  <tr><td><a href="https://github.com/Deatron01/NKVGM1EMNF-GM1_LA_AT_Eng">NKVGM1EMNF-GM1_LA_AT_Eng</a></td><td><sub><samp>COURSEWORK</samp></sub></td><td>Generative AI.</td></tr>
  <tr><td><a href="https://github.com/Deatron01/NIXSG1LBNE-SZTGUI_LA_02">NIXSG1LBNE-SZTGUI_LA_02</a></td><td><sub><samp>COURSEWORK</samp></sub></td><td>Software technology &amp; GUI design.</td></tr>
  <tr><td><a href="https://github.com/Deatron01/NKXBATHBNE-BevAdTud_EA_MI1">NKXBATHBNE-BevAdTud_EA_MI1</a></td><td><sub><samp>COURSEWORK</samp></sub></td><td>Introduction to data science.</td></tr>
  <tr><td><a href="https://github.com/Deatron01/Cpluszplusz-NSWCPVHBNF">Cpluszplusz-NSWCPVHBNF</a></td><td><sub><samp>COURSEWORK</samp></sub></td><td>C++.</td></tr>
</table>
</details>

### <samp>03 — STACK</samp>

<table>
  <tr><td><samp>LANGUAGES</samp></td><td><picture><source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i=python,cs,ts,js,cpp,php,latex&perline=10&theme=light" /><img src="https://skillicons.dev/icons?i=python,cs,ts,js,cpp,php,latex&perline=10&theme=dark" alt="Python · C# · TypeScript · JavaScript · C++ · PHP · LaTeX" height="40" /></picture></td></tr>
  <tr><td><samp>SYSTEMS</samp></td><td><picture><source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i=ros,unity,godot,blender,electron,fastapi,nodejs&perline=10&theme=light" /><img src="https://skillicons.dev/icons?i=ros,unity,godot,blender,electron,fastapi,nodejs&perline=10&theme=dark" alt="ROS / ROS 2 · Unity XR · Godot · Blender · Electron · FastAPI · Node.js" height="40" /></picture><br /><sub>+ OpenXR</sub></td></tr>
  <tr><td><samp>DATA</samp></td><td><picture><source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i=postgres&perline=10&theme=light" /><img src="https://skillicons.dev/icons?i=postgres&perline=10&theme=dark" alt="PostgreSQL" height="40" /></picture><br /><sub>+ Parquet · MinIO · vector search / RAG · local LLMs (Ollama)</sub></td></tr>
  <tr><td><samp>TOOLING</samp></td><td><picture><source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i=git,docker,linux,githubactions,vscode&perline=10&theme=light" /><img src="https://skillicons.dev/icons?i=git,docker,linux,githubactions,vscode&perline=10&theme=dark" alt="Git · Docker · Linux · GitHub Actions · VS Code" height="40" /></picture><br /><sub>+ WSL2</sub></td></tr>
</table>

### <samp>04 — ACTIVITY</samp>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Deatron01/Deatron01/output/snake-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Deatron01/Deatron01/output/snake-light.svg" />
    <img alt="Contribution graph being eaten by a snake" src="https://raw.githubusercontent.com/Deatron01/Deatron01/output/snake-light.svg" />
  </picture>
</p>

<img src="./assets/divider.svg" width="100%" alt="" />

<p align="center">
  <img src="./assets/icon.png" width="56" alt="Dea" /><br />
  <sub><i>Little chaos in a quiet mind.</i></sub><br />
  <sub><samp>DESIGN WORK LIVES AT <a href="https://deawebdesign.netlify.app/">DEAWEBDESIGN.NETLIFY.APP</a></samp></sub>
</p>
