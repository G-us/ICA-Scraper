#!/usr/bin/env python
import sys
import PySimpleGUI as sg


layout = [
          [sg.Button('ICA', button_color=('white', 'red'), key='ICA'),
           sg.Button('Coop', button_color=('white', 'green'), key='COOP')]
          ]

window = sg.Window("Select Website", layout, auto_size_buttons=False, default_button_element_size=(12,1), use_default_focus=False, finalize=True)


while True:
    event, values = window.read(timeout=100)
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'ICA':
        import ICAScraper
        print("ICA selected")
        window.close()
    if event == 'COOP':
        import CoopScraper
        print("Coop selected")
        window.close()
