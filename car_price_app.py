import tkinter as tk
from tkinter import ttk, messagebox
import pickle


def format_value(value):
    if value >= 10000000:
        return f"{value / 10000000:.2f} Cr"
    elif value >= 100000:
        return f"{value / 100000:.2f} Lakhs"
    else:
        return f"{value:,.0f}" if value >= 1000 else str(value)


# Load model and scaler
with open('./saved_models/RandomForestRegressor.pkl', 'rb') as f:
    model = pickle.load(f)

with open('./saved_scaling/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)


def validate_number(value, value_type):
    if value == '':
        raise ValueError('All fields are required')
    try:
        if value_type == 'int':
            return int(value)
        if value_type == 'float':
            return float(value)
    except Exception:
        raise ValueError(f"Enter a valid {value_type} value")


def pred_price():
    try:
        vehicle_age = validate_number(vehicle_age_var.get(), 'int')
        km_driven = validate_number(km_driven_var.get(), 'int')
        mileage = validate_number(mileage_var.get(), 'float')
        engine = validate_number(engine_var.get(), 'int')
        max_power = validate_number(max_power_var.get(), 'float')
        seats = validate_number(seats_var.get(), 'int')

        if not (1 <= seats <= 7):
            raise ValueError('Seats must be 1–7')

        input_values = [vehicle_age, km_driven, mileage, engine, max_power, seats]

        seller_map = {'Dealer': [1, 0, 0], 'Individual': [0, 1, 0], 'Trustmark Dealer': [0, 0, 1]}
        fuel_map = {
            'CNG': [1, 0, 0, 0, 0], 'Diesel': [0, 1, 0, 0, 0],
            'Electric': [0, 0, 1, 0, 0], 'LPG': [0, 0, 0, 1, 0], 'Petrol': [0, 0, 0, 0, 1]
        }
        transmission_map = {'Automatic': [1, 0], 'Manual': [0, 1]}

        input_values.extend(seller_map[seller_var.get()])
        input_values.extend(fuel_map[fuel_var.get()])
        input_values.extend(transmission_map[transmission_var.get()])

        if len(input_values) != 16:
            raise ValueError('Input vector size mismatch')

        progress_var.set(50)
        root.update_idletasks()

        scaled = scaler.transform([input_values])
        prediction_raw = model.predict(scaled)[0]
        pred_text = f"₹ {format_value(prediction_raw)}"

        price_label.config(text=pred_text, foreground='#00FF8C')
        status_label.config(text='Prediction successful ✅', foreground='white')
        progress_var.set(100)

        log_text.config(state='normal')
        log_text.insert('end', f"✓ {car_name_var.get() or 'Car'} predicted as {pred_text}\n")
        log_text.see('end')
        log_text.config(state='disabled')

    except Exception as err:
        price_label.config(text='Error in input', foreground='red')
        status_label.config(text=f'Error: {err}', foreground='orange')
        messagebox.showerror('Validation Error', str(err))
        progress_var.set(0)


def clear_inputs():
    for var in [car_name_var, vehicle_age_var, km_driven_var, mileage_var, engine_var, max_power_var, seats_var]:
        var.set('')
    seller_var.set('Dealer')
    fuel_var.set('Petrol')
    transmission_var.set('Manual')
    price_label.config(text='Predicted Price: ₹ 0', foreground='white')
    status_label.config(text='Enter values and click Predict', foreground='lightgray')
    progress_var.set(0)


root = tk.Tk()
root.title('Car Price Predictor')
root.geometry('1100x760')
root.configure(bg='#0F172A')
root.resizable(False, False)

style = ttk.Style(root)
style.theme_use('clam')
style.configure('TLabel', background='#EDEDED', foreground='#1F2937', font=('Segoe UI', 12))
style.configure('Header.TLabel', font=('Segoe UI', 30, 'bold'), foreground='#0F766E', background='#EDEDED')
style.configure('TButton', font=('Segoe UI', 12, 'bold'), padding=10, background='#10B981', foreground='white')
style.configure('TEntry', fieldbackground='white', foreground='#1F2937', font=('Segoe UI', 11))
style.configure('TRadiobutton', background='#EDEDED', foreground='#1F2937', font=('Segoe UI', 11))

root.configure(bg='#EDEDED')

header = ttk.Label(root, text='Car Price Predictor', style='Header.TLabel')
header.pack(pady=20)

main_frame = ttk.Frame(root, padding=20, style='Card.TFrame')
main_frame.pack(fill='both', expand=True)

left_frame = ttk.Frame(main_frame, style='Card.TFrame')
left_frame.grid(row=0, column=0, padx=15, pady=5, sticky='n')

right_frame = ttk.Frame(main_frame, style='Card.TFrame')
right_frame.grid(row=0, column=1, padx=10, pady=5, sticky='n')

fields = [
    ('Car Name', 'car_name'),
    ('Vehicle Age (years)', 'vehicle_age'),
    ('KM Driven', 'km_driven'),
    ('Mileage (kmpl)', 'mileage'),
    ('Engine (cc)', 'engine'),
    ('Max Power (bhp)', 'max_power'),
    ('Seats', 'seats')
]

car_name_var = tk.StringVar()
vehicle_age_var = tk.StringVar()
km_driven_var = tk.StringVar()
mileage_var = tk.StringVar()
engine_var = tk.StringVar()
max_power_var = tk.StringVar()
seats_var = tk.StringVar()

vars_map = {
    'car_name': car_name_var,
    'vehicle_age': vehicle_age_var,
    'km_driven': km_driven_var,
    'mileage': mileage_var,
    'engine': engine_var,
    'max_power': max_power_var,
    'seats': seats_var,
}

for idx, (lbl, key) in enumerate(fields):
    ttk.Label(left_frame, text=lbl + ':').grid(row=idx, column=0, sticky='w', pady=5)
    ttk.Entry(left_frame, textvariable=vars_map[key], width=28).grid(row=idx, column=1, pady=5, padx=5)

seller_var = tk.StringVar(value='Dealer')
fuel_var = tk.StringVar(value='Petrol')
transmission_var = tk.StringVar(value='Manual')

selector_frame = ttk.LabelFrame(left_frame, text='Options', padding=16, style='Card.TFrame')
selector_frame.grid(row=len(fields), column=0, columnspan=2, pady=12, sticky='we')

# seller combobox
ttk.Label(selector_frame, text='Seller Type').grid(row=0, column=0, sticky='w', padx=5)
seller_combo = ttk.Combobox(selector_frame, textvariable=seller_var, values=['Dealer', 'Individual', 'Trustmark Dealer'], state='readonly', width=18)
seller_combo.grid(row=0, column=1, padx=8, pady=4, sticky='w')

# fuel combobox
ttk.Label(selector_frame, text='Fuel Type').grid(row=1, column=0, sticky='w', padx=5, pady=(10, 0))
fuel_combo = ttk.Combobox(selector_frame, textvariable=fuel_var, values=['CNG', 'Diesel', 'Electric', 'LPG', 'Petrol'], state='readonly', width=18)
fuel_combo.grid(row=1, column=1, padx=8, pady=(10, 0), sticky='w')

# transmission combobox
ttk.Label(selector_frame, text='Transmission').grid(row=2, column=0, sticky='w', padx=5, pady=(10, 0))
transmission_combo = ttk.Combobox(selector_frame, textvariable=transmission_var, values=['Automatic', 'Manual'], state='readonly', width=18)
transmission_combo.grid(row=2, column=1, padx=8, pady=(10, 0), sticky='w')

button_frame = ttk.Frame(left_frame, padding=(0, 15))
button_frame.grid(row=len(fields) + 1, column=0, columnspan=2)

predict_btn = ttk.Button(button_frame, text='Predict Price', command=pred_price)
predict_btn.grid(row=0, column=0, padx=12)

clear_btn = ttk.Button(button_frame, text='Clear', command=clear_inputs)
clear_btn.grid(row=0, column=1, padx=12)

about_btn = ttk.Button(button_frame, text='About', command=lambda: messagebox.showinfo('About', 'Car Price Predictor\nVersion 1.1\nDeveloped for friendly app UX'))
about_btn.grid(row=0, column=2, padx=12)

result_frame = ttk.LabelFrame(right_frame, text='Result', padding=18, style='Card.TFrame')
result_frame.grid(row=0, column=0, sticky='nsew')

price_label = ttk.Label(result_frame, text='Predicted Price: ₹ 0', font=('Segoe UI', 28, 'bold'), foreground='#0F766E')
price_label.pack(pady=(8, 16))

status_label = ttk.Label(result_frame, text='Enter values and click Predict', font=('Segoe UI', 12), foreground='#6B7280')
status_label.pack(pady=(2, 10))

progress_var = tk.IntVar(value=0)
progress_bar = ttk.Progressbar(result_frame, orient='horizontal', length=360, mode='determinate', variable=progress_var)
progress_bar.pack(pady=10)

# Separation
sep = ttk.Separator(result_frame, orient='horizontal')
sep.pack(fill='x', pady=8)
log_frame = ttk.LabelFrame(right_frame, text='Activity Log', padding=10)
log_frame.grid(row=1, column=0, pady=12, sticky='nsew')

log_text = tk.Text(log_frame, width=40, height=18, bg='white', fg='#1F2937', wrap='word', borderwidth=1, relief='solid', font=('Segoe UI', 10))
log_text.pack(fill='both', expand=True)
log_text.config(state='disabled')

status_bar = ttk.Label(root, text='Ready', anchor='w', font=('Segoe UI', 10), background='#020617', foreground='white')
status_bar.pack(side='bottom', fill='x')

clear_inputs()

root.mainloop()
