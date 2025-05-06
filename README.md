This is a command line-based todo app inspired by linux pass and my llm scripts (like leviathan, tutorialize, ask, twig, etc.)

Motivation for this project:
- todo apps on the command line have existed for a long time, as well as implementations that store in a text-based format.
- my experience with the Mentor project showed the benefit of building my work environment as I do my daily work.
- I want to scale this idea to how I store, take notes, and complete tasks more broadly. Obsidian can be the GUI counterpart to this, and implementation is trivial given Obsidian being a wrapper around text files.
- This is "building the airplane as we are flying it" and a new approach to work. The idea here is that I spend 20% of my work day editing my work environment, with outsize performance benefits of 50%.

### Metalearning goals
- click CLI framework

### Use cases
- command line:
 - create a task: `todo follow up with Zapier -p ! -s blocked`
 - create a task (NLP): `todo follow up with zapier, high priority, blocked, before next Tuesday`
- shell: every command available that you have through `todo ____` on command line
 - advanced commands like building projects, adding / accessing documents
- obsidian: rework todo in main todo (changes in that markdown file get realized in database); work with daily mds as well
- ad hoc scripting: attaching work flows / data flows etc. into the mix; importing todo list into various convenience functions + AI implementations 

### Architecture
- python package (with setup.py entry points)
- postgres backend (for saving tasks, metadata, and everything else)
- markdown file in obsidian vault. A main todo file mirrors tasks saved in postgres; allows for manual editing of the todo list. Can contain hidden uuids. Other markdown files keyed to particular days can be pre-populated.
- vector document store in the backend (postgres or chroma)

### Task creation syntax
task: natural language
tag: #work
project: +project
status: -s
- todo (default if not specified)
- doing or in-progress
- blocked / waiting for
- done or completed
priority: -p l/m/h OR ! !! !!!
date: -d YYYY-MM-DD

