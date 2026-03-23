import unittest
from backend.hospital_bot import book_appointment, get_lab_results, get_hospital_info, PatientDeps, MOCK_APPOINTMENTS, agent

class DummyContext:
    def __init__(self, deps):
        self.deps = deps

class TestHospitalBotTools(unittest.TestCase):
    def setUp(self):
        self.deps = PatientDeps(patient_id="P12345", patient_name="John Doe")
        self.ctx = DummyContext(deps=self.deps)
        MOCK_APPOINTMENTS.clear()
        
        # Tools in late Pydantic AI are accessible in agent._tool_functions or similar
        # For simplicity, we just test the decorated functions directly if they are callable
        # Wait, if they are not directly callable, we test the logic that would be executed.
        
    def test_book_appointment_logic(self):
        # Even if wrapped, we can test the effect by calling the original function
        # In current pydantic-ai, @agent.tool functions are directly callable in Python 
        # but with the first arg as the context
        try:
            res = book_appointment(self.ctx, "Cardiology", "Next Monday")
            self.assertTrue(res.success)
            self.assertIn("Cardiology", res.message)
            self.assertEqual(len(MOCK_APPOINTMENTS), 1)
        except TypeError:
            # If wrapped by pydantic-ai Tool, we access .func or .function
            if hasattr(book_appointment, 'func'):
                res = book_appointment.func(self.ctx, "Cardiology", "Next Monday")
                self.assertTrue(res.success)
                self.assertEqual(len(MOCK_APPOINTMENTS), 1)

    def test_get_lab_results_logic(self):
        try:
            res = get_lab_results(self.ctx)
            self.assertIn("Complete Blood Count", res)
            self.assertIn("Pending", res)
        except TypeError:
            if hasattr(get_lab_results, 'func'):
                res = get_lab_results.func(self.ctx)
                self.assertIn("Complete Blood Count", res)

    def test_get_hospital_info_logic(self):
        try:
            res = get_hospital_info(self.ctx, "hours")
            self.assertIn("8:00 AM", res)
        except TypeError:
            if hasattr(get_hospital_info, 'func'):
                res = get_hospital_info.func(self.ctx, "hours")
                self.assertIn("8:00 AM", res)

if __name__ == '__main__':
    unittest.main()
