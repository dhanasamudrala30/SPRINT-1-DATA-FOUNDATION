import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./Component/Login.jsx";
import ResetPassword from "./Component/ResetPassword.jsx";
import Dashboard from "./Component/Dashboard.jsx";
import Dashboard1 from "./Component/Dashboard1.jsx";
import Dashboard2 from "./Component/Dashboard2.jsx";
import EmployeeProfile from './Component/Employeeprofile';
import DocumentManagement from "./Component/Documentmanagement.jsx";
import EmployeeDirectory from "./Component/Employeedirectory.jsx";
import DepartmentRoleAssignment from "./Component/DepartmentRoleAssignment.jsx";
import AttendanceTracking from "./Component/AttendanceTracking.jsx";
import ShiftRoster from "./Component/ShiftRoster.jsx";
import LeavePolicy from "./Component/LeavePolicy.jsx";
import HolidayCalendar from "./Component/HolidayCalendar.jsx";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/dashboard1" element={<Dashboard1 />} />
        <Route path="/dashboard2" element={<Dashboard2 />} />
        <Route path="/employee-profile" element={<EmployeeProfile />} />
        <Route path="/document-management" element={<DocumentManagement />} />
        <Route path="/employee-directory" element={<EmployeeDirectory />} />
        <Route path="/department-role-assignment" element={<DepartmentRoleAssignment />} />
        <Route path="/attendance-tracking" element={< AttendanceTracking />} />
        <Route path="/shift-roster" element={<ShiftRoster />} />
        <Route path="/leavepolicy" element={<LeavePolicy />} />
        <Route path="/holiday-calendar" element={<HolidayCalendar />} />

       
      </Routes>
    </Router>
  );
}

export default App;