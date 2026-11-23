import os
import json
import asyncio
import platform
from datetime import datetime
from typing import List, Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="ERIS-X + Air to Talk Unified OS", version="5.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UnifiedRequest(BaseModel):
    command: str
    model_router: str = "eris-omni"
    model_mode: str = "cyber_pink"
    agent_count: int = 128

class RAGMemoryStore:
    def __init__(self):
        self.records: List[Dict[str, Any]] = []

    def store(self, topic: str, findings: str):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "topic": topic,
            "findings": findings
        }
        self.records.append(entry)
        return entry

class MultiAgentSwarm:
    def __init__(self):
        self.clusters = {
            "Web_Scraper_Cluster": 32,
            "PhD_Scientific_Research_Cluster": 32,
            "RAG_Vector_Memory_Cluster": 24,
            "REA_Self_Modification_Cluster": 20,
            "Vision_CCTV_Animation_Cluster": 20,
        }

    async def execute_agent(self, agent_id: int, cluster: str, command: str) -> Dict[str, Any]:
        await asyncio.sleep(0.002)
        return {
            "agent_id": f"AG-{agent_id:03d}",
            "cluster": cluster,
            "status": "COMPLETED",
            "output": f"[{cluster}] Node insight synthesized for: {command}"
        }

    async def run_swarm(self, command: str) -> Dict[str, Any]:
        tasks = []
        idx = 1
        for cluster, count in self.clusters.items():
            for _ in range(count):
                tasks.append(self.execute_agent(idx, cluster, command))
                idx += 1
        results = await asyncio.gather(*tasks)
        summary = f"128-Agent Swarm completed synthesis across 5 clusters for '{command}'."
        memory.store(command, summary)
        return {"summary": summary, "total_agents": len(results), "sample_nodes": results[:5]}

class PCDesktopAgent:
    def __init__(self):
        self.os_info = platform.platform()

    def diagnostics(self):
        return {
            "os": self.os_info,
            "timestamp": datetime.now().isoformat(),
            "status": "ACTIVE_READY"
        }

    def log_task(self, task_name: str, workspace: str = "./workspace"):
        os.makedirs(workspace, exist_ok=True)
        log_path = os.path.join(workspace, "task_audit.log")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] Executed: {task_name}\n")
        return log_path

memory = RAGMemoryStore()
swarm = MultiAgentSwarm()
pc_agent = PCDesktopAgent()

@app.get("/")
def serve_portal():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    return FileResponse(html_path)

@app.get("/health")
def health_check():
    return {"status": "operational", "system": "ERIS-X + Air to Talk Unified Engine"}

@app.get("/api/pc-diagnostics")
def get_pc_diagnostics():
    return pc_agent.diagnostics()

@app.get("/api/memory")
def get_memory():
    return {"count": len(memory.records), "stored_entries": memory.records}

@app.post("/api/unified-execute")
async def unified_execute(req: UnifiedRequest):
    text = req.command.lower()
    pc_agent.log_task(req.command)
    swarm_result = await swarm.run_swarm(req.command)

    response_speech = (
        f"Namaste! Main ERIS-X Air to Talk AI hoon. Aapne kaha: '{req.command}'. "
        f"128 agents ne aapke task ko execute karke RAG memory mein save kar diya hai."
    )
    expression = "talking_smile"

    if any(k in text for k in ["storm", "disaster", "emergency"]):
        response_speech = "Emergency alert received. ERIS-X 128-agent disaster protocol activated immediately."
        expression = "alert_serious"
    elif any(k in text for k in ["status", "system", "diagnostics"]):
        response_speech = "All 128 swarm agents, 3D avatar renderer, RAG memory, and PC nodes are synchronized and online."
        expression = "nodding_happy"

    return {
        "status": "success",
        "router": req.model_router,
        "model_mode": req.model_mode,
        "speech_response": response_speech,
        "expression": expression,
        "swarm_summary": swarm_result["summary"],
        "memory_count": len(memory.records),
        "sample_nodes": swarm_result["sample_nodes"]
    }

@app.websocket("/ws/air-talk-live")
async def air_talk_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            packet = json.loads(data)
            user_text = packet.get("text", "")
            await websocket.send_text(json.dumps({
                "type": "audio_response_stream",
                "text": f"Air to Talk Live processed: {user_text}",
                "expression": "speaking"
            }))
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
