from fastapi import FastAPI
from app.routes import books, auth, member, circulation, fines, reports, payments, reservations

app = FastAPI(title="Library Management System")

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(member.router)
app.include_router(circulation.router)
app.include_router(fines.router)
app.include_router(reports.router)
app.include_router(payments.router)
app.include_router(reservations.router)
