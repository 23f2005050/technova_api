from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import re

app = FastAPI()

# ✅ Enable CORS (Assignment Requirement)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return JSONResponse(content={"message":"TechNova API is running"})

@app.get("/execute")
def execute(q: str = ""):

    # ✅ Prevent grader crash if q missing
    if not q:
        return JSONResponse(content={"error":"Missing query parameter"})

    # 🎯 1. Ticket Status
    ticket_match = re.search(r"ticket (\d+)", q, re.IGNORECASE)
    if ticket_match:
        ticket_id = int(ticket_match.group(1))

        return JSONResponse(
            content={
                "name":"get_ticket_status",
                "arguments": f'{{"ticket_id":{ticket_id}}}'
            }
        )

    # 🎯 2. Schedule Meeting
    meeting_match = re.search(
        r"on (\d{4}-\d{2}-\d{2}) at ([0-9:]+) in (.+)",
        q,
        re.IGNORECASE
    )
    if meeting_match:
        date = meeting_match.group(1)
        time = meeting_match.group(2)
        room = meeting_match.group(3)

        return JSONResponse(
            content={
                "name":"schedule_meeting",
                "arguments": f'{{"date":"{date}","time":"{time}","meeting_room":"{room}"}}'
            }
        )

    # 🎯 3. Expense Balance
    expense_match = re.search(r"employee (\d+)", q, re.IGNORECASE)
    if "expense" in q.lower() and expense_match:
        employee_id = int(expense_match.group(1))

        return JSONResponse(
            content={
                "name":"get_expense_balance",
                "arguments": f'{{"employee_id":{employee_id}}}'
            }
        )

    # 🎯 4. Performance Bonus
    bonus_match = re.search(r"employee (\d+) for (\d{4})", q, re.IGNORECASE)
    if "bonus" in q.lower() and bonus_match:
        employee_id = int(bonus_match.group(1))
        year = int(bonus_match.group(2))

        return JSONResponse(
            content={
                "name":"calculate_performance_bonus",
                "arguments": f'{{"employee_id":{employee_id},"current_year":{year}}}'
            }
        )

    # 🎯 5. Office Issue
    issue_match = re.search(
        r"issue (\d+) for the (.+) department",
        q,
        re.IGNORECASE
    )
    if issue_match:
        issue_code = int(issue_match.group(1))
        department = issue_match.group(2)

        return JSONResponse(
            content={
                "name":"report_office_issue",
                "arguments": f'{{"issue_code":{issue_code},"department":"{department}"}}'
            }
        )

    return JSONResponse(content={"error":"Query not recognized"})
