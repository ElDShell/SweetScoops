# SweetScoops

SweetScoops is a dynamic and user-friendly e-commerce website for selling ice cream. The website is fully functional with a backend that supports product management, a shopping cart system, order processing, and integration with PayPal for payments. Below is an overview of the project:

## Features

### Frontend
- The frontend design was initially provided, and I made several enhancements:
  - [Link to the original frontend](https://htmlcodex.com/ice-cream-shop-website-template/)
  - Modified the navigation bar for better usability.
  - Adjusted the color scheme for a fresh, vibrant look.
  - Updated some images to enhance the overall aesthetic.

### Backend
The backend of SweetScoops was includes the following functionalities:

#### Home Page
- A welcoming homepage introducing SweetScoops and showcasing featured products.

#### Products Page
- Displays a list of available ice cream products.
- Customers can add items to their cart directly from this page.
- AJAX is used to dynamically load more products without refreshing the page.

#### Gallery Page
- A gallery showcasing ice cream with filtering options to refine the product view.
- Pagination is implemented to improve navigation and performance.

#### Cart
- A shopping cart where customers can:
  - View the items they’ve added.
  - Adjust the quantity of each product.
  - See the total value of their cart in real-time.

#### Checkout and Orders
- After finalizing the cart, customers can proceed to checkout.
- Orders can be managed with the following options:
  - Accept: Provides payment options like credit card, PayPal, or cash on delivery.
  - Cancel: Removes the order.
- PayPal integration (in sandbox mode) is implemented for secure transactions.

## Technology Stack
- **Backend:** Django
- **Frontend Enhancements:** HTML, CSS, JavaScript
- **AJAX:** Used for dynamic product loading
- **Payment Integration:** PayPal (sandbox mode)

## How to Use
i will publish the website in pyhtonanywhere soon . you can access it by visiting the website link.
## PayPal Sandbox Setup
To test the PayPal integration, use the provided sandbox credentials. Replace the credentials in the settings file with your PayPal sandbox client ID and secret if necessary.

## Future Improvements
- Add user authentication for personalized shopping experiences.
- Enhance the frontend for a more seamless user experience.
- Expand payment options beyond PayPal and cash on delivery.

## Contributions
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments
- Special thanks to the open-source community for providing resources and tools that made this project possible.

Feel free to explore, contribute, and enjoy SweetScoops!
