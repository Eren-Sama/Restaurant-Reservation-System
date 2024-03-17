import PySimpleGUI as sg
import webbrowser
import time

class Reservation:
    def __init__(self, name, contact, date, time, guests, table_type, special_requests):
        self.name = name
        self.contact = contact
        self.date = date
        self.time = time
        self.guests = guests
        self.table_type = table_type
        self.special_requests = special_requests

    def calculate_price(self):
        if self.table_type == 'Exclusive Table':
            return 1000
        elif self.table_type == 'Luxury Table':
            return 700
        elif self.table_type == 'Deluxe Table':
            return 500
        elif self.table_type == 'Modern Table':
            return 350
        elif self.table_type == 'Classic Table':
            return 250
        else:
            return 0

class ReservationWindow:
    def __init__(self):
        sg.theme('Reddit')
        self.layout = self.create_layout()
        self.window = sg.Window('Restaurant Reservation System', self.layout)

    def create_layout(self):
        layout = [
            [sg.Text('Name:'), sg.InputText(key='-NAME-')],
            [sg.Text('Contact:'), sg.InputText(key='-CONTACT-')],
            [sg.Text('Date:'), sg.InputText(key='-DATE-', enable_events=True), sg.CalendarButton('Choose Date', target='-DATE-', format='%Y-%m-%d')],
            [sg.Text('Time:'), sg.InputText(key='-TIME-', size=(10, 1), enable_events=True)],
            [sg.Text('Number of Guests:'), sg.Spin([i for i in range(1, 11)], initial_value=1, key='-GUESTS-')],
            [sg.Text('Table Type:'), sg.Combo(['Exclusive Table', 'Luxury Table', 'Deluxe Table', 'Modern Table', 'Classic Table'], key='-TABLETYPE-')],
            [sg.Text('Special Requests:'), sg.InputText(key='-SPECIAL-')],
            [sg.Button('Book'), sg.Button('Cancel')],
        ]
        return layout

    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event == 'Book':
                reservation = self.get_reservation(values)
                if reservation:
                    self.redirect_to_paypal(reservation)
                    self.reset_fields()

        self.window.close()

    def get_reservation(self, values):
        name = values['-NAME-'].strip()
        contact = values['-CONTACT-'].strip()
        date = values['-DATE-']
        time = values['-TIME-']
        guests = values['-GUESTS-']
        table_type = values['-TABLETYPE-']
        special_requests = values['-SPECIAL-'].strip()

        if not all([name, contact, date, time]):
            sg.popup('Please fill in all fields.', title='Error')
            return None
        if len(contact) != 10 or not contact.isdigit():
            sg.popup('Phone number should be a 10-digit number.', title='Error')
            return None

        return Reservation(name, contact, date, time, guests, table_type, special_requests)

    def redirect_to_paypal(self, reservation):
        price = reservation.calculate_price()
        payment_url = f'https://www.paypal.com?amount={price}&currency=USD'
        webbrowser.open(payment_url)
        sg.popup('Redirecting to PayPal for payment...', title='Payment Gateway')

        # Here, you would wait for the user to complete the payment on PayPal and return to your site.
        # After successful payment, you can confirm the booking and display the full bill.

        self.show_success_message(reservation)

    def show_success_message(self, reservation):
        price = reservation.calculate_price()
        success_msg = f"Your Table Has Been Successfully Booked!\n\nName: {reservation.name}\nContact: {reservation.contact}\nDate: {reservation.date}\nTime: {reservation.time}\nGuests: {reservation.guests}\nTable Type: {reservation.table_type}\nSpecial Requests: {reservation.special_requests}\n\nPrice: {price}"
        popup = sg.popup(success_msg, title='Success', auto_close=True, auto_close_duration=5)

    def reset_fields(self):
        self.window['-NAME-'].update('')
        self.window['-CONTACT-'].update('')
        self.window['-DATE-'].update('')
        self.window['-TIME-'].update('')
        self.window['-GUESTS-'].update(1)
        self.window['-TABLETYPE-'].update('')
        self.window['-SPECIAL-'].update('')

if __name__ == '__main__':
    reservation_system = ReservationWindow()
    reservation_system.run()
