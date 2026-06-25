import React, { useState } from 'react';
import "./../styles/HolidayCalendar.css";
import { useNavigate } from 'react-router-dom';

const HolidayCalendar = () => {
    const navigate = useNavigate();
    const currentYear = new Date().getFullYear();
    const [selectedMonth, setSelectedMonth] = useState(null);

    const holidays = {
        0: [1, 26],
        2: [8],
        4: [1],
        7: [15],
        9: [2],
        10: [14],
        11: [25],
    };

    const months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];

    const renderCalendar = (monthIndex) => {
        const daysInMonth = new Date(currentYear, monthIndex + 1, 0).getDate();
        const firstDay = new Date(currentYear, monthIndex, 1).getDay();

        const days = [];
        for (let i = 0; i < firstDay; i++) {
            days.push(<div key={`empty-${i}`} className="day empty"></div>);
        }

        for (let day = 1; day <= daysInMonth; day++) {
            const isHoliday = holidays[monthIndex]?.includes(day);
            days.push(
                <div
                    key={day}
                    className={`day ${isHoliday ? 'holiday' : ''}`}
                >
                    {day}
                </div>
            );
        }
        return days;
    };

    return (

        <div className="calendar-container">
            <button className="back-btn" onClick={() => navigate('/dashboard2')}>
                ← Back
            </button>
            <h2 className="title">{currentYear} Holiday Calendar</h2>
            <div className="months-grid">
                {months.map((month, index) => (
                    <div
                        key={month}
                        className={`month-card ${selectedMonth === index ? 'active' : ''}`}
                        onClick={() => setSelectedMonth(index)}
                    >
                        <h3>{month}</h3>
                        <div className="days-grid">
                            {renderCalendar(index)}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default HolidayCalendar;
