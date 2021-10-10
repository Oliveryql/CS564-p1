python my_parser.py ebay_data/items-*.json
sort item.dat | uniq > Uniqueitem.dat
sort user.dat | uniq > UniqueUser.dat
sort auction.dat | uniq > UniqueAuction.dat
sort category.dat | uniq > UniqueCategory.dat
