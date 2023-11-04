   ## myKart
   *Intended to develop an e-store*


## Prerequisities
- Python 3.8
- Mongodb

## How to start?
```
1. Clone the repository
      git clone https://github.com/mohitarora3/Fashion-Store
      cd  ecommerce

2. Create and activate a virtual environment
      virtualenv env 
      source env/Scripts
      activate
   
3. Install requirements:-
      pip install -r requirements.txt
    
4. Run the application
      python run.py
      
5. Open http://127.0.0.1.5000./

```

## Technologies used:-
 - Python
 - Flask
 - Mongodb
 - Html
 - CSS
 - Javascript


 ## Current Functionalities:-
- User, seller can register and sign in.
- Multiple Sellers can sell their products.
- Customer can browse products.
- Filter products based on brand, gender, price and discount.
- Customer can rate and review product.
- Customer can add/remove products from wishlist.
- Customer can move products from wishlist to cart.
- Customer can add/ remove items from cart.
- Customer can place order.
- Customer can get additional discounts on purchase.
- Customer can cancel an order.

## Under Development:
- Searching Items
- Online payment gateway
- Add to cart
- Social Connections

## dependabot.yml
 To get started with Dependabot version updates, you'll need to specify which
 package ecosystems to update and where the package manifests are located.
 Please see the documentation for all configuration options:
 https://help.github.com/github/administering-a-repository/configuration-options-for-dependency-updates

 version: 2
 updates:
   - package-ecosystem: "pip" # See documentation for possible values
     directory: "/" # Location of package manifests
     schedule:
       interval: "daily"
     Allow up to 2 open pull requests for pip dependencies
     open-pull-requests-limit: 2
