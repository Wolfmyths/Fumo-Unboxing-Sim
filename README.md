# Fumo Unboxing Simulator

This was my first project ever in Python that I found on my PC and decided
to clean it up to be more usable. It may not be 100% organized but I tried my best.

**I will personally not work on this project but will continue to maintain it for the time being**

I have multiple issues posted so if anyone wants to go take a look
and improve the project be my guest.

## Contributing

Some things to keep in mind when working on the project:

+ This project uses PySide6 as it's GUI framework
+ Anything style-related should go in `style.qss`
+ The data of fumos are in `fumo-data.json` and were designed to be able to be customizable

### Adding a fumo to the database

Add a dictionary to the `fumo-data.json`, here is an example of what it should look like
*available rarities can be found in `consts.py`*
```json
{
    "rarity": "string",
    "name": "string",
    "img": "url/img.png",
    "silouette": "url/img.png",
    "amount": 0,
    "recent": -1
}
```

### Color Pallet

+ #0B1354
+ #165BAA
+ #A155B9
+ #F765A3
+ #FFA4B6
+ #F9D1D1
+ #C6848D

# Credits
Fumo photos where taken and edited from 
https://fumo.website/fumo_list.html
