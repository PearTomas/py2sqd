import sys
import os
import subprocess

# Global list to store trace events as (caller, callee)
trace_events = []

def tracefunc(frame, event, arg):
    # Record only function call events
    if event == "call":
        code = frame.f_code
        func_name = code.co_name
        # Get caller name if available; otherwise use 'main'
        caller_frame = frame.f_back
        caller = caller_frame.f_code.co_name if caller_frame else "main"
        trace_events.append((caller, func_name))
    return tracefunc

def generate_plantuml(trace_events, puml_filename="./diagram.puml"):
    """Generate a simple PlantUML script from trace events."""
    lines = ["@startuml"]
    # Each event is output as "caller -> callee: call"
    for caller, callee in trace_events:
        lines.append(f"{caller} -> {callee}: call")
    lines.append("@enduml")
    plantuml_script = "\n".join(lines)
    with open(puml_filename, "w") as f:
        f.write(plantuml_script)
    return puml_filename

def run_plantuml(puml_file, output_svg="~/sequence_diagram.svg"):
    """Run PlantUML to generate an SVG file."""
    # Ensure that plantuml.jar is available in the working directory
    cmd = ["java", "-jar", "./plantuml-gplv2-1.2025.2.jar", "-tsvg", puml_file]
    subprocess.run(cmd, check=True)
    # By default, PlantUML creates an SVG with the same base name as the PUML file
    generated_svg = os.path.splitext(puml_file)[0] + ".svg"
    os.rename(generated_svg, output_svg)
    return output_svg

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_sequence_diagram.py <target_script.py>")
        sys.exit(1)

    target_script = sys.argv[1]

    # TODO: Generate PUML file from the target script to generate Squences Diagram NOT TRIVIAL :/
    sys.settrace(tracefunc)
    try:
        with open(target_script, "rb") as f:
            code = compile(f.read(), target_script, 'exec')
            exec(code, {})  # Run the target Python code in an empty namespace
    except Exception as e:
        print("Error while running target script:", e)
    finally:
        # Stop tracing to avoid further recording
        sys.settrace(None)

    # Generate the PlantUML file from the recorded events
    puml_file = generate_plantuml(trace_events)
    # Generate the SVG using PlantUML (requires plantuml.jar and Java)
    svg_file = run_plantuml(puml_file)
    print(f"Sequence diagram generated: {svg_file}")

if __name__ == "__main__":
    main()
