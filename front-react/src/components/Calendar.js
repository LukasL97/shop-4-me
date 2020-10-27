import React from 'react'
import PropTypes from 'prop-types'
import FullCalendar from '@fullcalendar/react'
import interactionPlugin from '@fullcalendar/interaction';
import timeGridPlugin from '@fullcalendar/timegrid';

const Calendar = (props) => {
  return <div className='calendar'>
    <FullCalendar
      plugins={[ timeGridPlugin, interactionPlugin ]}
      initialView="timeGridWeek"
      allDaySlot={false}
      slotMinTime={"08:00:00"}
      slotMaxTime={"22:00:00"}
      weekends={true}
      locale={"en"}
      dayHeaderFormat={{
        day: 'numeric',
        month: 'numeric'
      }}
      slotLabelFormat={{
        hour: 'numeric',
        minute: '2-digit',
        omitZeroMinute: true,
        hour12: false
      }}
      events={props.data.map((data) => ({
        ...data,
      }))}
    />
  </div>
}

const AvailabilityCalendar = (props) => {
  var now = new Date();

  var calendarData = [
    {start: "2020-10-25T14:30", end: "2020-10-25T16:00", nrequests: 0},
    {start: "2020-10-25T17:00", end: "2020-10-25T20:00", nrequests: 5},
    {start: "2020-10-27T17:30", end: "2020-10-27T19:30"},
    {start: "2020-10-29T17:00", end: "2020-10-29T19:00"},
  ].map((data) => ({
    start: data.start,
    end: data.end,
    editable: new Date(data.start) >= now,
    title: new Date(data.end) < now ? 
        (data.nrequests == 0 ? 
          "Skipped" :
          "You helped " + data.nrequests + " household" + (data.nrequests == 1 ? "!" : "s!")) :
      (new Date(data.start) < now ?
        "Delivering" :
        "Available"),
    backgroundColor: new Date(data.end) < now ? "#474" : (new Date(data.start) < now ? "#7F7" : "#77F")
  }))

  var thanks = {weekly: 42, monthly: 123, yearly: 123}
  var thanksComponent;
  if (thanks.weekly > 0) {
    thanksComponent = <AppreciationHeader thanks={thanks.weekly} intervalName={"week"}/>
  } else if (thanks.monthly > 0) {
    thanksComponent = <AppreciationHeader thanks={thanks.monthly} intervalName={"month"}/>
  } else if (thanks.yearly > 0) {
    thanksComponent = <AppreciationHeader thanks={thanks.yearly} intervalName={"year"}/>
  } else {
    thanksComponent = <AppreciationHeader />
  }
  return <>
    {thanksComponent}
    <Calendar
      from={"2020-10-20"}
      to={"2020-10-30"}
      data={calendarData}
    />
  </>
}

const AppreciationHeader = (props) => {
  return props.thanks? 
    <h1>You have got <b>{props.thanks}</b> Thank You's this {props.intervalName}! Your help is appreciated!</h1> :
    <h1>Your help is appreciated!</h1>
}

//Calendar.propTypes = {}

export default AvailabilityCalendar
