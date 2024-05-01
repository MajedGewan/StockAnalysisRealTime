import pytz

def timezone_to_offset(timezone):
    # Get the timezone object
    tz = pytz.timezone(timezone)
    
    # Get the current offset
    current_offset = tz.utcoffset(pytz.datetime.datetime.now())
    
    # Convert offset to hours and minutes
    hours = current_offset.days * 24 + current_offset.seconds // 3600
    minutes = (current_offset.seconds % 3600) // 60
    
    # Construct the offset string
    offset_string = f"UTC {hours:+03d}:{minutes:02d}"
    
    return offset_string