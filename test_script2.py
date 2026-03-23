from backend.hospital_bot import book_appointment, PatientDeps
class DummyCtx:
    def __init__(self):
        self.deps = PatientDeps("P12345", "John Doe")
print(type(book_appointment))
print(book_appointment(DummyCtx(), "Cardiology", "Tomorrow"))
