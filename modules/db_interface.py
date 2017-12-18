import pandas as pd
import os

base = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
flight_details_path = base + '/data/flight_details.csv'
booking_details_path = base + '/data/booking_details.csv'


def get_all_bookings(psid):
    """
    get all the booking details for a given psid
    :param psid: string psid
    :return: dataframe of all bookings
    """
    booking_data = pd.read_csv(booking_details_path)
    booking_data = booking_data.loc[booking_data['psid'] == int(psid)]
    return booking_data


print get_all_bookings(psid=1691246400937758)


def get_cancel_booking_ids(psid):
    """
    return the flight numbers of confirmed flights to cancel
    :param psid: strin psid
    :return: list of all booking_ids
    """

    booking_data = get_all_bookings(psid=psid)
    booking_ids = booking_data.loc[booking_data['status'] == 'confirmed']["booking_id"]
    return list(booking_ids)


print get_cancel_booking_ids(psid=1691246400937758)


def get_webcheckin_booking_ids(psid):
    """
        return the flight numbers of confirmed flights to webcheckin
        :param psid: strin psid
        :return: list of all booking_ids
    """

    booking_data = get_all_bookings(psid=psid)
    booking_ids = booking_data.loc[booking_data['status'] == 'confirmed']["booking_id"]
    return list(booking_ids)


print get_webcheckin_booking_ids(psid=1691246400937758)


def get_feedback_booking_ids(psid):
    """
        return the flight numbers of confirmed flights to give feedback for
        :param psid: strin psid
        :return: list of all booking_ids
    """

    booking_data = get_all_bookings(psid=psid)
    booking_ids = booking_data.loc[booking_data['status'] == 'completed']["booking_id"]
    return list(booking_ids)


print get_feedback_booking_ids(psid=1691246400937758)


def get_flights_origin_dest(origin,destination):
    """
    get all flights between a given origin and destination
    :param origin: string origin city
    :param destination: string destination city
    :return: list of airline names and departure
    """

    flights_data = pd.read_csv(flight_details_path)
    data = flights_data.loc[flights_data["destination"] == str(destination)]
    data_1 = data.loc[data["origin"] == str(origin)]
    list_of_flights = []
    for index, row in data_1.iterrows():
        list_of_flights.append(row["flight_number"] + " at " + str(row["departure_time"]) + " hrs")
    print "\n\n\nlist of flights"
    return list_of_flights


print get_flights_origin_dest(u"London", u"Paris")


def add_booking(booking_data):
    """
    add a new booking to database
    :param booking_data: dict booking_data
    :return: status of adding the data to database
    """

    booking_data_all = pd.read_csv(booking_details_path)
    try:
        booking_data_all = booking_data_all.append(booking_data,ignore_index=True)
        booking_data_all.to_csv(booking_details_path,index=False)
        print 'added to DB'
        return 'successfully added to DB'
    except:
        print 'not added to DB'
        return 'failed in adding to DB'


def update_booking(data_dict,type):
    """
    update the booking details database for cancellation/webcheckin requests
    :param data_dict: dict of relevant data
    :param type: cancel/webcheckin
    :return: status of updating database
    """

    booking_data_all = pd.read_csv(booking_details_path)
    print booking_data_all
    if type == 'cancel':
        booking_id = data_dict['booking_id']
        df1 = booking_data_all.loc[booking_data_all["booking_id"] != int(booking_id)]
        df_temp = booking_data_all.loc[booking_data_all["booking_id"] == int(booking_id)]
        temp_dict = df_temp.to_dict(orient='list')
        temp_dict['status'] = ['cancelled']
        df_temp_1 = pd.DataFrame(temp_dict)
        df_res = df1.append(df_temp_1)
        print df_res
        df_res.to_csv(booking_details_path)
        return 'database updated after cancel request'

    elif type == 'webcheckin':
        booking_id = data_dict['booking_id']
        seat_pref = data_dict['seat_pref']
        seat_number = data_dict['seat_number']
        df1 = booking_data_all.loc[booking_data_all["booking_id"] != int(booking_id)]
        df_temp = booking_data_all.loc[booking_data_all["booking_id"] == int(booking_id)]
        temp_dict = df_temp.to_dict(orient='list')
        temp_dict['seat_pref'] = [seat_pref]
        temp_dict['seat_number'] = [seat_number]
        temp_dict['status'] = ['checkedin']
        df_temp_1 = pd.DataFrame(temp_dict)
        df_res = df1.append(df_temp_1)
        print df_res
        df_res.to_csv(booking_details_path)
        return 'database updated after webcheckin request'

    elif type == 'feedback':
        booking_id = data_dict['booking_id']
        feedback = data_dict['feedback']
        df1 = booking_data_all.loc[booking_data_all["booking_id"] != int(booking_id)]
        df_temp = booking_data_all.loc[booking_data_all["booking_id"] == int(booking_id)]
        temp_dict = df_temp.to_dict(orient='list')
        temp_dict['feedback'] = [feedback]
        df_temp_1 = pd.DataFrame(temp_dict)
        df_res = df1.append(df_temp_1)
        print df_res
        df_res.to_csv(booking_details_path)
        return 'database updated after feedback request'