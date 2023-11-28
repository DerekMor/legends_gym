# Testing Documentation

## Manual Testing
Manual tests have been performed and documented to ensure the usability and proper function of the website. This testing involved trying multiple options on each page to try to find if any of the website functions were not working as expected. These were all documented in Github annd the list can be found <a href="https://github.com/DerekMor/legends_gym/issues?q=+label%3ATest+"> HERE </a>. <br> An example of manual testing of one of the pages on the site can seen below.
<img src="media/manual.png" alt="Manual Testing screenshot">

## Html Validation
### Home page
<img src="media/homehtml.png" alt="Validation Testing screenshot">

### One time code page
<img src="media/codehtml.png" alt="Validation Testing screenshot">

### Profile page
<img src="media/profilehtml.png" alt="Validation Testing screenshot">

### All Products page
<img src="media/allproductshtml.png" alt="Validation Testing screenshot">

### Single Product page
<img src="media/singleproducthtml.png" alt="Validation Testing screenshot">

### Add Review page
<img src="media/reviewhtml.png" alt="Validation Testing screenshot">

### Logout page
<img src="media/logouthtml.png" alt="Validation Testing screenshot">

### Registration page
<img src="media/registerhtml.png" alt="Validation Testing screenshot">

### Login page
<img src="media/loginhtml.png" alt="Validation Testing screenshot">

### Cart page
<img src="media/carthtml.png" alt="Validation Testing screenshot">

### Checkout page
Here things get a little strange. My forms work spread across two divs like they are supposed to. The form will not submit if neither form is filled out and the payment section is side by side with the details form which is more visually appealing on larger screens. If I was to change the tags to fix these errors the form will work but the payment section will be in the same column as the details which is fine on mobile or the two forms will be independent and one can submit without the other being filled out. Because of this I am leaving it the way it is as the page is working the way it is supposed to over all screen sizes and page layouts.
<img src="media/checkouthtml.png" alt="Validation Testing screenshot">

### Checkout Success page
<img src="media/successhtml.png" alt="Validation Testing screenshot">

## CSS Validation
### base.css
<img src="media/basecss.png" alt="Validation Testing screenshot">

### checkout.css
<img src="media/checkoutcss.png" alt="Validation Testing screenshot">

## Python Validation
In all cases I could not solve the line too long issue from getting an error using an indent or a \ for an explicit continuation. It told me the new line was under indented until it got so far that it was over indented so the line too long were left in. The only way I could make the error dissapear on the validation was by indenting the continuation by a tab and then a space which broke my code so i chose working code over removing line too long errors.

### profiles/views.py
<img src="media/profileview.png" alt="Validation Testing screenshot">

### profiles/urls.py
<img src="media/profileurls.png" alt="Validation Testing screenshot">

### profiles/signals.py
<img src="media/profilesignals.png" alt="Validation Testing screenshot">

### profiles/models.py
<img src="media/profilemodels.png" alt="Validation Testing screenshot">

### products/views.py
<img src="media/productsviews.png" alt="Validation Testing screenshot">

### products/urls.py
<img src="media/productsurls.png" alt="Validation Testing screenshot">

### products/models.py
<img src="media/productsmodels.png" alt="Validation Testing screenshot">

### legends_gym/urls.py
<img src="media/legendsurls.png" alt="Validation Testing screenshot">

### home/views.py
<img src="media/homeviews.png" alt="Validation Testing screenshot">

### home/urls.py
<img src="media/homeurls.png" alt="Validation Testing screenshot">

### checkout/views.py
<img src="media/checkoutviews.png" alt="Validation Testing screenshot">

### checkout/urls.py
<img src="media/checkouturls.png" alt="Validation Testing screenshot">

### checkout/models.py
<img src="media/checkoutmodels.png" alt="Validation Testing screenshot">

### checkout/admin.py
<img src="media/checkoutadmin.png" alt="Validation Testing screenshot">

### cart/views.py
<img src="media/cartviews.png" alt="Validation Testing screenshot">

### cart/urls.py
<img src="media/carturls.png" alt="Validation Testing screenshot">

### cart/contexts.py
<img src="media/cartcontexts.png" alt="Validation Testing screenshot">

