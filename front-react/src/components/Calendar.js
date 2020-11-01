import React, { Component } from 'react'
import PropTypes from 'prop-types'
import FullCalendar, { render } from '@fullcalendar/react'
import interactionPlugin from '@fullcalendar/interaction';
import timeGridPlugin from '@fullcalendar/timegrid';
import Cookies from 'universal-cookie'
import axios from 'axios'

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

class AvailabilityCalendar extends Component {
	state = {
		calendarData: [],
		thanks: {weekly: 42, monthly: 123, yearly: 123}
	}
  
	componentDidMount() {
		this.populateCalendar()
	}

	populateCalendar() {
		const cookies = new Cookies();
	
		const url = 'http://localhost:5000/timeframes'
		axios({
			method: "POST",
			url: url, 
			data: {
				sessionId: cookies.get("access_token")
			}
		}).then((response) => {
			var now = new Date();
	
			const calendarData = response.data.map((timeframe) => ({
				...timeframe,
				nrequests: (timeframe.requests || []).length()
			})).map((timeframe) => ({
				start: timeframe.start,
				end: timeframe.end,
				editable: new Date(timeframe.start) >= now,
				title: new Date(timeframe.end) < now ? 
					(timeframe.nrequests == 0 ? 
					"Skipped" :
					"You helped " + timeframe.nrequests + " household" + (timeframe.nrequests == 1 ? "!" : "s!")) :
				(new Date(timeframe.start) < now ?
					"Delivering" :
					"Available"),
				backgroundColor: new Date(timeframe.end) < now ? "#474" : (new Date(timeframe.start) < now ? "#7F7" : "#77F")
			}))
			
			this.state.calendarData = calendarData
		})
	}

	render() {
		var thanks = this.state.thanks;
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
			data={this.state.calendarData}
			/>
		</>
	}
}

const AppreciationHeader = (props) => {
  return props.thanks? 
    <h1>You have got <b>{props.thanks}</b> Thank You's this {props.intervalName}! Your help is appreciated!</h1> :
    <h1>Your help is appreciated!</h1>
}

//Calendar.propTypes = {}

export default AvailabilityCalendar
