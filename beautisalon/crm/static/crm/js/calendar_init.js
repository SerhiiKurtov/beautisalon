document.addEventListener('DOMContentLoaded', function() {
    var calendarElements = document.querySelectorAll('[id^="calendar-"]');

    calendarElements.forEach(function(calendarEl) {
        var masterId = calendarEl.id.split('-')[1];

        var calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'timeGridWeek',
            locale: 'uk',
            slotMinTime: '09:00:00',
            slotMaxTime: '21:00:00',
            allDaySlot: false,          
            events: '/api/load_schedule/' + masterId + '/',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'timeGridWeek,dayGridMonth'
            },
            height: 'auto',
            nowIndicator: true,
            eventColor: '#14a119'
        });
        calendar.render();
    });
});