# Module to generate responses to user queries
import requests
import json
import classifier as cl
import entity_recognizer as en
import db_interface as dbi
import random

PAT = 'EAABZB3OScsuIBAFIN9SjJ2ZAqwvcAMMZCi4uDw62iZBgtLile75GND8sO8aUgv2TKlZAopbULPEwk3KvN7NanlTpU1H6HAukv8Fm6t6v8htSpWbJA2uWt3ZATzODuv55HTu7OzW0icmp5luudUFR6sCwbjB7C6qyE5VgwZA0s6xbQZDZD'


def get_user_details(detail_type, psid):
    """
    :param detail_type: list parameter describing detail. Ex. ['first_name', 'last_name'] and so on from API
    :param payload: all message call payload details
    :return: dict of all details
    """

    print "psid = " + str(psid)
    url = "https://graph.facebook.com/v2.6/" + str(psid)
    params = {"fields": ','.join(detail_type), "access_token": PAT}

    details = requests.get(url=url, params=params)
    return json.loads(details.text)


def gen_quick_reply(texts):
    """
    Generate a quick reply list of dictionaries given all the texts for the replies
    :param texts: list of quick replies string.
    :return: list of dictionaries for the quick replies field
    """
    quick_replies = []
    for text in texts:
        quick_replies.append({"content_type": "text", "title": text, "payload": text})
    quick_replies.append({"content_type": "text", "title": "Exit", "payload": "Exit"})
    return quick_replies


def gen_nlp_query_response(text, textclass, psid):
    """
    generate appropriate response to a given nlp query
    :param text: string text
    :param textclass: string class; book, cancel, webcheckin, feedback
    :return: string response
    """

    if textclass == 'book':
        origin_city = en.get_city_of_origin(text)
        destination_city = en.get_destination_city(text)
        date = en.get_date(text)
        time = en.get_time(text)
        start_time = None if len(time) == 0 else time[0]
        end_time = time[1] if len(time) == 2 else None
        airline = en.get_airline(text)
        print origin_city, destination_city, date
        details = ("Request Type: Book Ticket" + "\n" + "Origin: " + str(origin_city) + "\n" + "Destination: " + str(
            destination_city) + "\n" + "Date: " + str(date) + "\n" + "Airline Preference: " + str(airline) + "\n")

        try:
            booking_data = json.loads(open("booking_data_" + psid + ".txt", 'r').read())
            print "bookingdatatry"
            print booking_data,type(booking_data)
        except:
            print "bookingdatacatch"
            open("booking_data_" + psid + ".txt", 'w+').write("{}")
            booking_data = json.loads(open("booking_data_" + psid + ".txt", 'r').read())
            print booking_data,type(booking_data)

        print "\n\n\nbooking data\n\n\n"
        print booking_data,type(booking_data)
        print origin_city,destination_city,date
        booking_data["origin"] = str(origin_city)
        booking_data["destination"] = str(destination_city)
        booking_data["date_of_travel"] = str(date)
        # get the stage for the interactive CI to start from
        if not origin_city:
            stage = 'hi_21'
        elif not destination_city:
            stage = 'book_from_city_1'+'origin_1'
        elif not date:
            stage = 'book_to_city_1'+'dest_1'
        else:
            stage = 'booking_date_1'+'date_2'

        open("booking_data_" + psid + ".txt", 'w+').write(json.dumps(booking_data, indent=4))
        return details, stage

    elif textclass == 'cancel':
        pnr = en.get_pnr(text)
        details = "Request Type: Cancellation" + "\n" + "Booking ID: " + str(pnr) + "\n"

        cancel_data = json.loads(open("cancel_data_" + psid + ".txt", 'r').read())
        if not pnr:
            stage = 'hi_22'
        else:
            cancel_data["booking_id"] = pnr
            stage = 'cancel_select_1'

        open("cancel_data_" + psid + ".txt", 'w+').write(json.dumps(cancel_data, indent=4))
        return details, stage

    elif textclass == 'webcheckin':
        pnr = en.get_pnr(text)
        details = "Request Type: Web Check In" + "\n" + "Booking ID: " + str(pnr) + "\n"

        webcheckin_data = json.loads(open("webcheckin_data_" + psid + ".txt", 'r').read())

        if not pnr:
            stage = 'hi_23'
        else:
            webcheckin_data["booking_id"] = pnr
            stage = 'webcheckin_select_1'

        open("webcheckin_data_" + psid + ".txt", 'w+').write(json.dumps(webcheckin_data, indent=4))
        return details, stage

    elif textclass == 'feedback':
        airline = en.get_airline(text)
        pnr = en.get_pnr(text)
        details = "Request Type: Feedback on \nAirline Name: " + str(airline) + "\n"

        feedback_data = json.loads(open("feedback_data_" + psid + ".txt", 'r').read())
        if not pnr:
            stage = 'hi_24'
        else:
            feedback_data["booking_id"] = pnr
            stage = 'feedback_select_1'

        open("feedback_data_" + psid + ".txt", 'w+').write(json.dumps(feedback_data, indent=4))
        return details, stage


def gen_booking_id(booking_data):
    """
    return a unique booking id
    :param booking_data: dict booking_data
    :return: string booking_id
    """

    booking_id = str(random.randint(10000,99999))
    print '\n\n\nunique booking id' + booking_id
    return booking_id


def gen_ticket_details(booking_dict):
    """
    generate the final bill/flight details before confirmation from user
    :param booking_dict: dict booking details
    :return: string bill message to be sent to user
    """
    response = ""
    response = response + "Origin: " + booking_dict["origin"] + "\n"
    response = response + "Destination: " + booking_dict["destination"] + "\n"
    response = response + "Date: " + booking_dict["date_of_travel"] + "\n"
    response = response + "Flight Number: " + booking_dict["flight_number"] + "\n"
    response = response + "Passenger Name: " + booking_dict["name"] + "\n"
    response = response + "Email: " + booking_dict["email"] + "\n"
    response = response + "DOB: " + booking_dict["date_of_birth"] + "\n"
    response = response + "Insurance: " + booking_dict["insurance"] + "\n"
    response = response + "Seat Preference: " + booking_dict["seat_pref"] + "\n"
    response = response + "Seat Class: " + booking_dict["class"] + "\n"

    # calculate the final bill
    if booking_dict["class"] == "Economy":
        base_price = 120
    else:
        base_price = 180

    if booking_dict["insurance"] == 'Yes':
        insurance_price = 5
    else:
        insurance_price = 0

    if booking_dict["seat_pref"] != 'No':
        seat_price = 2
    else:
        seat_price = 0

    total_price = base_price + insurance_price + seat_price
    response = response + "Base Price: $" + str(base_price) + "\n"
    response = response + "Insurance Cost: $" + str(insurance_price) + "\n"
    response = response + "Seat Preference Cost: $" + str(seat_price) + "\n"
    response = response + "Total: $" + str(total_price) + "\n"

    return response


def gen_data_dict(text, payload, psid):
    """
    :param text: string value of text to be sent
    :param payload: full payload for extra info if necessary
    :return: data_dict: depending on type, quick replies and other API properties
    """

    # get the current state of chatbot execution
    curr_state = ""
    try:
        curr_state = str(open("program_state_" + psid + ".txt", 'r').read())
    except:
        curr_state = ""

    # create/save temp files for booking/cancel/webcheckin/feedback requests for each user
    try:
        booking_data = json.loads(open("booking_data_" + psid + ".txt", 'r').read())
    except:
        open("booking_data_" + psid + ".txt", 'w+').write("{}")
        booking_data = json.loads(open("booking_data_" + psid + ".txt", 'r').read())

    try:
        cancel_data = json.loads(open("cancel_data_" + psid + ".txt", 'r').read())
    except:
        open("cancel_data_" + psid + ".txt", 'w+').write("{}")
        cancel_data = json.loads(open("cancel_data_" + psid + ".txt", 'r').read())

    try:
        webcheckin_data = json.loads(open("webcheckin_data_" + psid + ".txt", 'r').read())
    except:
        open("webcheckin_data_" + psid + ".txt", 'w+').write("{}")
        webcheckin_data = json.loads(open("webcheckin_data_" + psid + ".txt", 'r').read())

    try:
        feedback_data = json.loads(open("feedback_data_" + psid + ".txt", 'r').read())
    except:
        open("feedback_data_" + psid + ".txt", 'w+').write("{}")
        feedback_data = json.loads(open("feedback_data_" + psid + ".txt", 'r').read())

    # exit strategy whenever user is confused - guide to user interactive messenger interface
    if 'hi_1' in curr_state and text == "Yes":
        user_details = get_user_details(['first_name'], psid=psid)
        data_dict = {
            "text": "Hi " + user_details['first_name'] + ". What would you like to do? Pick from the options below.",
            "quick_replies": gen_quick_reply(["Book Ticket", "Cancel Ticket", "Web Check In", "Feedback"])
        }
        # 4 different states of booking, cancellation, webcheckin and feedback - hi_2x for x = 1,2,3,4
        open("program_state_" + psid + ".txt", 'w+').write("hi_21 hi_22 hi_23 hi_24")

    # Always start with Hi
    elif text in ['hi', 'Hi', 'HI']:
        print "\n\n\n user details \n\n\n"
        user_details = get_user_details(['first_name'], psid=psid)
        data_dict = {
            "text": "Hi " + user_details['first_name'] + ". How can I help you?",
        }
        open("program_state_" + psid + ".txt", 'w+').write("nlp_1")

    elif 'nlp_1' in curr_state:
        text_class = cl.classify_text(text)
        print text_class
        response, stage = gen_nlp_query_response(text=text, textclass=text_class, psid=psid)
        print response
        data_dict = {
            "text": response + "Would you like to proceed?",
            "quick_replies": gen_quick_reply(["Yes", "No", "Try Again"])
        }
        open("program_state_" + psid + ".txt", 'w+').write("nlp_2 " + str(stage))

    elif 'nlp_2' in curr_state and text == 'No':
        user_details = get_user_details(['first_name'], psid=psid)
        data_dict = {
            "text": "Hi " + user_details['first_name'] + ". What would you like to do? Pick from the options below.",
            "quick_replies": gen_quick_reply(["Book Ticket", "Cancel Ticket", "Web Check In", "Feedback"])
        }
        open("booking_data_" + psid + ".txt", 'w+').write("{}")
        open("cancel_data_" + psid + ".txt", 'w+').write("{}")
        open("webcheckin_data_" + psid + ".txt", 'w+').write("{}")
        open("feedback_data_" + psid + ".txt", 'w+').write("{}")
        open("program_state_" + psid + ".txt", 'w+').write("hi_21 hi_22 hi_23 hi_24")

    elif 'nlp_2' in curr_state and text == 'Try Again':
        user_details = get_user_details(['first_name'], psid=psid)
        data_dict = {
            "text": "Hi " + user_details['first_name'] + ". How can I help you?",
        }
        open("program_state_" + psid + ".txt", 'w+').write("nlp_1")

    elif text == "Exit":
        data_dict = {
            "text": "Exited current workflow - say Hi to start again!",
            "quick_replies": gen_quick_reply(['Hi'])
        }
        open("booking_data_" + psid + ".txt", 'w+').write(json.dumps({}))
        open("program_state_" + psid + ".txt", 'w').write("")

    elif text == "Book Ticket" or ('hi_21' in curr_state and 'hi_22 hi_23 hi_24' not in curr_state):
        city_list = ["London", "Paris", "New York", "Hong Kong", "Berlin", "Munich"]  # Replace once pandas is set
        data_dict = {
            "text": "Choose your city of origin?",
            "quick_replies": gen_quick_reply(city_list)
        }
        open("program_state_" + psid + ".txt", 'w').write("book_from_city_1")

    elif 'book_from_city_1' in curr_state:
        city_list = ["London", "Paris", "New York", "Hong Kong", "Berlin",
                     "Munich"]  # Replace once pandas is set
        data_dict = {
            "text": "Choose your destination?",
            "quick_replies": gen_quick_reply(city_list)
        }
        if 'origin_1' not in curr_state:
            booking_data["origin"] = text
        open("booking_data_" + psid + ".txt", 'w+').write(json.dumps(booking_data, indent=4))
        open("program_state_" + psid + ".txt", 'w').write("book_to_city_1")

    elif 'book_to_city_1' in curr_state:
        data_dict = {
            "text": "Please enter the date of travel - in DD/MM/YYYY format only"
        }
        if 'dest_1' not in curr_state:
            booking_data["destination"] = text
        open("booking_data_" + psid + ".txt", 'w+').write(json.dumps(booking_data, indent=4))
        open("program_state_" + psid + ".txt", 'w').write("booking_date_1")

    elif 'booking_date_1' in curr_state:
        print booking_data["origin"],booking_data["destination"],type(booking_data["origin"])
        flights = dbi.get_flights_origin_dest(origin=booking_data["origin"], destination=booking_data["destination"])
        data_dict = {
            "text": "Please pick the flight of your choice.",
            "quick_replies": gen_quick_reply(flights)
        }
        if 'date_2' not in curr_state:
            booking_data["date_of_travel"] = text
        open("booking_data_" + psid + ".txt", 'w+').write(json.dumps(booking_data, indent=4))
        open("program_state_" + psid + ".txt", 'w').write("flight_select_1")

    elif 'flight_select_1' in curr_state:
        seat_styles = ["Economy", "Business"]  # Replace once pandas is set
        data_dict = {
            "text": "What is your category preference?",
            "quick_replies": gen_quick_reply(seat_styles)
        }
        booking_data["flight_number"] = text.split()[0]
        open("booking_data_" + psid + ".txt", 'w+').write(json.dumps(booking_data, indent=4))
        open("program_state_" + psid + ".txt", 'w').write("seat_pref_1")

    elif 'seat_pref_1' in curr_state:
        data_dict = {
            "text": "Would you like to select seats? (at $2)",
            "quick_replies": gen_quick_reply(["Yes", "No"])
        }
        booking_data["class"] = text
        open("booking_data_" + psid + ".txt", 'w+').write(json.dumps(booking_data, indent=4))
        open("program_state_" + psid + ".txt", 'w').write("seat_select_1")

    elif 'seat_select_1' in curr_state and text == 'Yes':
        seat_styles = ["Isle", "Window", "Middle"]
        data_dict = {
            "text": "What would be your seat preference?",
            "quick_replies": gen_quick_reply(seat_styles)
        }
        open("program_state_" + psid + ".txt", 'w').write("seat_select_2")

    elif 'seat_select_1' in curr_state or 'seat_select_2' in curr_state:
        data_dict = {
            "text": "Would you like travel insurance? (At $5)",
            "quick_replies": gen_quick_reply(["Yes", "No"])
        }
        if 'seat_select_2' in curr_state:
            seat_num = str(random.randint(1,30))
            if text == 'Isle':
                seat_number = seat_num + "c"
            elif text == 'Window':
                seat_number = seat_num + "a"
            else:
                seat_number = seat_num + "b"
        else:
            seat_number = "No"
        booking_data["seat_pref"] = text
        booking_data["seat_number"] = seat_number
        open("booking_data_" + psid + ".txt", 'w+').write(json.dumps(booking_data, indent=4))
        open("program_state_" + psid + ".txt", 'w').write("insurance_1")

    elif 'insurance_1' in curr_state:
        user_details = get_user_details(detail_type=["first_name", "last_name"], psid=psid)
        print user_details
        data_dict = {
            "text": "Enter the passenger name.",
            "quick_replies": gen_quick_reply([user_details['first_name'] + " " + user_details['last_name']])
        }
        booking_data["insurance"] = text
        open("booking_data_" + psid + ".txt", 'w+').write(json.dumps(booking_data, indent=4))
        open("program_state_" + psid + ".txt", 'w').write("passenger_name_1")

    elif 'passenger_name_1' in curr_state:
        data_dict = {
            "text": "Please enter the passenger's email address",
            "quick_replies": gen_quick_reply([])
        }
        booking_data["name"] = text
        open("booking_data_" + psid + ".txt", 'w+').write(json.dumps(booking_data, indent=4))
        open("program_state_" + psid + ".txt", 'w').write("passenger_email_1")

    elif 'passenger_email_1' in curr_state:
        data_dict = {
            "text": "Please enter the passenger's date of birth (in DD/MM/YYYY format)",
            "quick_replies": gen_quick_reply([])
        }
        booking_data["email"] = text
        open("booking_data_" + psid + ".txt", 'w+').write(json.dumps(booking_data, indent=4))
        open("program_state_" + psid + ".txt", 'w').write("passenger_dob_1")

    elif 'passenger_dob_1' in curr_state:
        booking_data["date_of_birth"] = text
        booking_details = gen_ticket_details(booking_data)
        data_dict = {
            "text": "Here are your booking details, would you like to confirm this purchase?\n\n" + booking_details + "\n\n The amount shall be deducted from your online wallet.",
            "quick_replies": gen_quick_reply(["Yes", "No"])
        }
        open("booking_data_" + psid + ".txt", 'w+').write(json.dumps(booking_data, indent=4))
        open("program_state_" + psid + ".txt", 'w').write("payment_conf_1"
                                                          )
    elif 'payment_conf_1' in curr_state and text == "Yes":
        booking_id_1 = gen_booking_id(booking_data=booking_data)
        data_dict = {
            "text": "Your booking is complete with booking ID - " + str(booking_id_1) + ". You may now type 'Hi' to start again!",
            "quick_replies": gen_quick_reply(["Hi"])
        }
        booking_data["booking_id"] = booking_id_1
        booking_data["status"] = 'confirmed'
        booking_data["checkin"] = 'No'
        booking_data["feedback"] = 'No'
        booking_data["psid"] = psid
        open("booking_data_" + psid + ".txt", 'w+').write(json.dumps(booking_data, indent=4))
        dbi.add_booking(booking_data=booking_data)
        open("program_state_" + psid + ".txt", 'w').write("")

    elif 'payment_conf_1' in curr_state and text == "No":
        data_dict = {
            "text": "Your booking has been stopped. Say Hi to start again!",
            "quick_replies": gen_quick_reply(["Hi"])
        }
        open("booking_data_" + psid + ".txt", 'w+').write(json.dumps({}, indent=4))
        open("program_state_" + psid + ".txt", 'w').write("")

    elif text == "Cancel Ticket" or ('hi_22' in curr_state and 'hi_23 hi_24' not in curr_state and 'hi_21' not in curr_state):
        booking_list = dbi.get_cancel_booking_ids(psid=psid)
        data_dict = {
            "text": "Which of the following bookings - Booking ID - would you like to cancel?",
            "quick_replies": gen_quick_reply(booking_list)
        }
        open("program_state_" + psid + ".txt", 'w').write("cancel_select_1")

    elif 'cancel_select_1' in curr_state:
        payment_options = ["Website Wallet"]
        data_dict = {
            "text": "Which mode of refund would you like?",
            "quick_replies": gen_quick_reply(payment_options)
        }
        try:
            booking_id = cancel_data["booking_id"]
            print "booking_id already given = " + str(booking_id)
        except:
            cancel_data["booking_id"] = text
            open("cancel_data_" + psid + ".txt", 'w+').write(json.dumps(cancel_data, indent=4))
        open("program_state_" + psid + ".txt", 'w').write("cancel_payment_1")

    elif 'cancel_payment_1' in curr_state:
        data_dict = {
            "text": "Your cancellation for Booking ID: " + str(cancel_data["booking_id"]) + " has been completed. You will be updated by mail! Say Hi to start again.",
            "quick_replies": gen_quick_reply(['Hi'])
        }
        dbi.update_booking(data_dict=cancel_data,type='cancel')
        open("program_state_" + psid + ".txt", 'w').write("")

    elif text == "Web Check In" or ('hi_23' in curr_state and 'hi_21 hi_22' not in curr_state and 'hi_24' not in curr_state):
        booking_list = dbi.get_webcheckin_booking_ids(psid=psid)
        data_dict = {
            "text": "Which of the following flight bookings - Booking ID - would you like to check into?",
            "quick_replies": gen_quick_reply(booking_list)
        }
        open("program_state_" + psid + ".txt", 'w').write("webcheckin_select_1")

    elif 'webcheckin_select_1' in curr_state:
        seat_types = ['Isle', 'Window', 'Middle']
        data_dict = {
            "text": "What is your seat preference?",
            "quick_replies": gen_quick_reply(seat_types)
        }
        try:
            booking_id = webcheckin_data["booking_id"]
            print "booking_id already given = " + str(booking_id)
        except:
            webcheckin_data["booking_id"] = text
            open("webcheckin_data_" + psid + ".txt", 'w+').write(json.dumps(webcheckin_data, indent=4))
        open("program_state_" + psid + ".txt", 'w').write("webcheckin_seat_style_1")

    elif 'webcheckin_seat_style_1' in curr_state:
        if text == 'Isle':
            seat_number = str(random.randint(1,30)) + "c"
        elif text == 'Window':
            seat_number = str(random.randint(1, 30)) + "a"
        else:
            seat_number = str(random.randint(1, 30)) + "b"
        data_dict = {
            "text": "Webcheck in for Booking ID " + str(webcheckin_data["booking_id"]) + " is complete! Your seat number is - " + str(seat_number) + ". Say Hi to start again!",
            "quick_replies": gen_quick_reply(['Hi'])
        }
        webcheckin_data["seat_pref"] = text
        webcheckin_data["seat_number"] = seat_number
        dbi.update_booking(data_dict=webcheckin_data,type='webcheckin')
        open("webcheckin_data_" + psid + ".txt", 'w+').write(json.dumps(webcheckin_data, indent=4))
        open("program_state_" + psid + ".txt", 'w').write("")

    elif text == "Feedback" or ('hi_24' in curr_state and 'hi_21 hi_22 hi_23' not in curr_state):
        booking_list = dbi.get_feedback_booking_ids(psid=psid)
        data_dict = {
            "text": "Which of the following bookings - Booking ID - would you like to give feedback for?",
            "quick_replies": gen_quick_reply(booking_list)
        }
        open("program_state_" + psid + ".txt", 'w').write("feedback_select_1")

    elif 'feedback_select_1' in curr_state:
        data_dict = {
            "text": "Please enter your complete feedback for Booking ID " + text,
            "quick_replies": gen_quick_reply(['Very Good','Good','Average','Bad','Very Bad'])
        }
        try:
            booking_id = feedback_data["booking_id"]
            print "booking_id already given = " + str(booking_id)
        except:
            feedback_data["booking_id"] = text
            open("feedback_data_" + psid + ".txt", 'w+').write(json.dumps(feedback_data, indent=4))
        open("program_state_" + psid + ".txt", 'w').write("feedback_input_1")

    elif 'feedback_input_1' in curr_state:
        data_dict = {
            "text": "Your feedback for Booking ID " + str(feedback_data["booking_id"]) + " has been recorded. You will be communicated to via email for the same. Thank you.",
            "quick_replies": gen_quick_reply(['Hi'])
        }
        feedback_data["feedback"] = text
        dbi.update_booking(data_dict=feedback_data, type='feedback')
        open("feedback_data_" + psid + ".txt", 'w+').write(json.dumps(feedback_data, indent=4))
        open("program_state_" + psid + ".txt", 'w').write("")

    else:
        data_dict = {
            "text": "Sorry I dont get it, lets start again. Would you like to use our interactive system?",
            "quick_replies": gen_quick_reply(["Yes", "No"])
        }
        open("program_state_" + psid + ".txt", 'w').write("hi_1")

    print json.loads(open("booking_data_" + psid + ".txt", 'r').read())
    print json.loads(open("cancel_data_" + psid + ".txt", 'r').read())
    print json.loads(open("webcheckin_data_" + psid + ".txt", 'r').read())
    print json.loads(open("feedback_data_" + psid + ".txt", 'r').read())
    print str(open("program_state_" + psid + ".txt", 'r').read())

    return data_dict
