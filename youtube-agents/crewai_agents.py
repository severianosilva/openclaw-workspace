#!/usr/bin/env python3
"""YouTube Money Agents - CrewAI Implementation"""

from crewai import Agent, Task, Crew, Process
from pathlib import Path
import json

BASE_DIR = Path(__file__).parent

# ============== AGENTES CREWAI ==============

researcher = Agent(
    role="YouTube Topic Researcher",
    goal="Find high-CPM, trending topics for YouTube monetization",
    backstory="Expert in YouTube SEO and keyword research. Specializes in identifying profitable niches with CPM > $20.",
    verbose=True,
    allow_delegation=False
)

scriptwriter = Agent(
    role="YouTube Script Writer", 
    goal="Create engaging, SEO-optimized video scripts using proven formulas",
    backstory="Professional content writer with 10+ years creating viral YouTube content. Expert in Hook-Story-Offer format.",
    verbose=True,
    allow_delegation=False
)

designer = Agent(
    role="Visual Designer",
    goal="Create eye-catching thumbnails and channel branding that increase CTR",
    backstory="Graphic designer specializing in YouTube thumbnails with 5M+ views generated. Expert in color psychology.",
    verbose=True,
    allow_delegation=False
)

video_editor = Agent(
    role="Video Editor",
    goal="Produce professional YouTube videos automatically with FFmpeg",
    backstory="Video editing expert using FFmpeg and AI tools. Specializes in fast turnaround times.",
    verbose=True,
    allow_delegation=False
)

publisher = Agent(
    role="YouTube Publisher",
    goal="Upload and optimize videos for maximum reach and monetization",
    backstory="YouTube automation specialist with proven growth strategies. Expert in SEO and thumbnails.",
    verbose=True,
    allow_delegation=False
)

# ============== TAREFAS ==============

def create_tasks(niche="finances"):
    """Cria as tarefas para o crew"""
    
    research_task = Task(
        description=f"Research 10 profitable topics in {niche} niche with CPM > $15",
        agent=researcher,
        expected_output="JSON with topics, CPM estimates, and keywords"
    )
    
    script_task = Task(
        description="Write an 8-minute engaging script with hook in first 15 seconds",
        agent=scriptwriter,
        expected_output="Full script with timestamps, chapters, and CTAs"
    )
    
    design_task = Task(
        description="Create thumbnail with face + text + colors that increase click-through",
        agent=designer,
        expected_output="PNG thumbnail and branding guide"
    )
    
    edit_task = Task(
        description="Assemble video with intro, b-roll, and outro using FFmpeg",
        agent=video_editor,
        expected_output="MP4 video file"
    )
    
    publish_task = Task(
        description="Upload with optimized title, description, and tags",
        agent=publisher,
        expected_output="YouTube video URL"
    )
    
    return [research_task, script_task, design_task, edit_task, publish_task]

# ============== CREW ==============

def run_crew(niche="finances"):
    """Executa o crew completo"""
    
    tasks = create_tasks(niche)
    
    crew = Crew(
        agents=[researcher, scriptwriter, designer, video_editor, publisher],
        tasks=tasks,
        process=Process.sequential,
        verbose=2
    )
    
    result = crew.kickoff()
    return result

if __name__ == "__main__":
    print("=" * 50)
    print("YouTube Money Agents - CrewAI Mode")
    print("=" * 50)
    
    print("\n[INFO] Para executar:")
    print("1. pip install crewai langchain langchain-openai")
    print("2. Configure OPENAI_API_KEY")
    print("3. python crewai_agents.py")
    
    # Salvar configuração para importação
    config = {
        "crew_name": "YouTube Money Agents",
        "version": "1.0",
        "agents": ["Researcher", "Scriptwriter", "Designer", "VideoEditor", "Publisher"],
        "process": "sequential"
    }
    
    with open(BASE_DIR / "crew.yaml", 'w') as f:
        f.write(f"name: {config['crew_name']}\n")
        f.write(f"version: {config['version']}\n")