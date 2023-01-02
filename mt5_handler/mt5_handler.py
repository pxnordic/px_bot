import MetaTrader5
from dataclasses import dataclass
import os
from log import log
import json


@dataclass
class mt5_handle:
    mt5_json_file: str

    def __post_init__(self):
        self.logger = log.mylog(__name__)
        if os.path.exists(self.mt5_json_file):
            f = open(self.mt5_json_file, "r")
            project_settings = json.load(f)
            f.close()
        else:
            self.logger.error('JSON config file for MT% does not exist')

        self.uname = project_settings["username"]
        self.pword = project_settings["password"]
        self.server = project_settings["server"]
        self.mt5Pathway = project_settings["mt5Pathway"]
        self.symbols = project_settings["symbols"]

    def start_mt5(self):
        uname = int(self.uname)
        pword = str(self.pword)
        trading_server = str(self.server)
        filepath = str(self.mt5Pathway)

        # Attempt to start MT5
        if MetaTrader5.initialize(login=uname, password=pword, server=trading_server, path=filepath):
            print("Trading Bot Starting")
            # Login to MT5
            if MetaTrader5.login(login=uname, password=pword, server=trading_server):
                print("Trading Bot Logged in and Ready to Go!")
                return True
            else:
                print("Login Fail")
                quit()
                return PermissionError
        else:
            print("MT5 Initialization Failed")
            quit()
            return ConnectionAbortedError

    def initialize_symbols(self):
        symbol_array = self.symbols
        # Get a list of all symbols supported in MT5
        all_symbols = MetaTrader5.symbols_get()
        # Create an array to store all the symbols
        symbol_names = []
        # Add the retrieved symbols to the array
        for symbol in all_symbols:
            symbol_names.append(symbol.name)

        # Check each symbol in symbol_array to ensure it exists
        for provided_symbol in symbol_array:
            if provided_symbol in symbol_names:
                # If it exists, enable
                if MetaTrader5.symbol_select(provided_symbol, True):
                    print(f"Sybmol {provided_symbol} enabled")
                else:
                    return ValueError
            else:
                return SyntaxError

        # Return true when all symbols enabled
        return True

    def place_order(self, order_type, symbol, volume, price, stop_loss, take_profit, comment):
        # If order type SELL_STOP
        if order_type == "SELL_STOP":
            order_type = MetaTrader5.ORDER_TYPE_SELL_STOP
        elif order_type == "BUY_STOP":
            order_type = MetaTrader5.ORDER_TYPE_BUY_STOP
        # Create the request
        request = {
            "action": MetaTrader5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": round(price, 3),
            "sl": round(stop_loss, 3),
            "tp": round(take_profit, 3),
            "type_filling": MetaTrader5.ORDER_FILLING_RETURN,
            "type_time": MetaTrader5.ORDER_TIME_GTC,
            "comment": comment
        }
        # Send the order to MT5
        order_result = MetaTrader5.order_send(request)
        # Notify based on return outcomes
        if order_result[0] == 10009:
            print(f"Order for {symbol} successful")
        else:
            print(f"Error placing order. ErrorCode {order_result[0]}, Error Details: {order_result}")
        return order_result

    def cancel_order(self, order_number):
        # Create the request
        request = {
            "action": MetaTrader5.TRADE_ACTION_REMOVE,
            "order": order_number,
            "comment": "Order Removed"
        }
        # Send order to MT5
        order_result = MetaTrader5.order_send(request)
        return order_result

    def modify_position(self, order_number, symbol, new_stop_loss, new_take_profit):
        # Create the request
        request = {
            "action": MetaTrader5.TRADE_ACTION_SLTP,
            "symbol": symbol,
            "sl": new_stop_loss,
            "tp": new_take_profit,
            "position": order_number
        }
        # Send order to MT5
        order_result = MetaTrader5.order_send(request)
        if order_result[0] == 10009:
            return True
        else:
            return False

    def set_query_timeframe(self, timeframe: str):
        if timeframe == "M1":
            return MetaTrader5.TIMEFRAME_M1
        elif timeframe == "M2":
            return MetaTrader5.TIMEFRAME_M2
        elif timeframe == "M3":
            return MetaTrader5.TIMEFRAME_M3
        elif timeframe == "M4":
            return MetaTrader5.TIMEFRAME_M4
        elif timeframe == "M5":
            return MetaTrader5.TIMEFRAME_M5
        elif timeframe == "M6":
            return MetaTrader5.TIMEFRAME_M6
        elif timeframe == "M10":
            return MetaTrader5.TIMEFRAME_M10
        elif timeframe == "M12":
            return MetaTrader5.TIMEFRAME_M12
        elif timeframe == "M15":
            return MetaTrader5.TIMEFRAME_M15
        elif timeframe == "M20":
            return MetaTrader5.TIMEFRAME_M20
        elif timeframe == "M30":
            return MetaTrader5.TIMEFRAME_M30
        elif timeframe == "H1":
            return MetaTrader5.TIMEFRAME_H1
        elif timeframe == "H2":
            return MetaTrader5.TIMEFRAME_H2
        elif timeframe == "H3":
            return MetaTrader5.TIMEFRAME_H3
        elif timeframe == "H4":
            return MetaTrader5.TIMEFRAME_H4
        elif timeframe == "H6":
            return MetaTrader5.TIMEFRAME_H6
        elif timeframe == "H8":
            return MetaTrader5.TIMEFRAME_H8
        elif timeframe == "H12":
            return MetaTrader5.TIMEFRAME_H12
        elif timeframe == "D1":
            return MetaTrader5.TIMEFRAME_D1
        elif timeframe == "W1":
            return MetaTrader5.TIMEFRAME_W1
        elif timeframe == "MN1":
            return MetaTrader5.TIMEFRAME_MN1

    def query_historic_data(self, symbol, timeframe, number_of_candles):
        # Convert the timeframe into an MT5 friendly format
        mt5_timeframe = self.set_query_timeframe(timeframe)
        # Retrieve data from MT5
        rates = MetaTrader5.copy_rates_from_pos(symbol, mt5_timeframe, 1, number_of_candles)
        return rates

    def get_open_orders(self):
        orders = MetaTrader5.orders_get()
        order_array = []
        for order in orders:
            order_array.append(order[0])
        return order_array

    def get_open_positions(self):
        # Get position objects
        positions = MetaTrader5.positions_get()
        # Return position objects
        return positions
