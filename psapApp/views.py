# from .models import Student
# Assuming you have a Student model defined for your database table
# from .models import StdApplyAdmission
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from .models import StdInfoTable
from django.db import connection
from .models import StdInfoTable
from .models import Admission
from .forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse
from django.db import connection as conn

from django.contrib import messages

# Create your views here.

# main page index file
email = ''
password = ''


def index(request):
    return render(request, 'index.html')

# loginasUNI


def uniOrStd(request):
    return render(request, 'uniorstd.html')


def loginasUni(request):
    return render(request, 'loginasUni.html')


def loginasStd(request):
    # Add your view logic here
    return render(request, 'loginasStd.html')


def registerasUniPage(request):
    # Add your view logic here
    return render(request, 'registerasUni.html')


def registerasStd(request):
    # Add your view logic here
    return render(request, 'registerasStd.html')


def stdHome(request):
    # Add your view logic here
    if request.session.get('authenticated') == True:
        email = request.session.get('email')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT first_name FROM psapapp_stdinfotable WHERE email=%s", [email])
        stdName = cursor.fetchone()[0]
        return render(request, 'stdHome.html', {'stdName': stdName})


from .models import AppliedForAdmissionForm
from django.http import JsonResponse

def stdApplied(request):
    if request.session.get('authenticated') == True:
        email = request.session.get('email')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT first_name, id FROM psapapp_stdinfotable WHERE email=%s", [email])
        row = cursor.fetchone()
        if row:
            stdName = row[0]
            std_id = row[1]
        if request.method == 'POST':
            # Get the form data from the POST request
            university_name = request.POST.get('university')
            campus = request.POST.get('campus')
            program = request.POST.get('program')
            department = request.POST.get('department')
            required_test = request.POST.get('required_test')
            test_obtained_marks = request.POST.get('test_obtained_marks')
            test_total_marks = request.POST.get('test_total_marks')
            fees_slip = request.FILES.get('fees_slip')

            # Assuming you have a model named AppliedForAdmissionForm
            try:
                # Save the form data into the table
                admission_form = AppliedForAdmissionForm.objects.create(
                    university_name=university_name,
                    campus=campus,
                    program=program,
                    department=department,
                    required_test=required_test,
                    test_obtained_marks=test_obtained_marks,
                    test_total_marks=test_total_marks,
                    fees_slip=fees_slip,
                    std_email=email,
                    student_info_id=std_id,
                )
                admission_form.save(d)
                return JsonResponse({'success': 'Form data saved successfully'}, status=200)

            except Exception as e:
                # Handle exceptions or errors if necessary
                return JsonResponse({'error': 'Error saving form data'}, status=500)

        # Return a bad request response if the request method is not POST
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    else:
        return redirect('university_login/')





def stdNewApplication(request):
    # Add your view logic here
    email = request.session.get('email')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT first_name FROM psapapp_stdinfotable WHERE email=%s", [email])
    stdName = cursor.fetchone()[0]
    admissions = Admission.objects.all()
    admission_data = []
    for admission in admissions:

        data = {
            'university_name': admission.university_name,
            'department': admission.departments,
            'campus': admission.campus,
            "admission_test": admission.admission_test,
            'program': admission.program,
        }
        admission_data.append(data)
    context = {
        'admissions': admissions,
        'stdName': stdName,
    }
    return render(request, 'stdNewApplication.html', {'admissions': admission_data, 'stdName': stdName})


def uniHome(request):
    if request.session.get('authenticated') == True:
        email = request.session.get('email')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT university_name FROM psapapp_uniinfotable WHERE email=%s", [email])
        uniName = cursor.fetchone()[0]
        admissions = Admission.objects.filter(university_name=uniName)
        context = {
            'admissions': admissions,
            'uniName': uniName,
        }
        return render(request, 'uniHome.html', context)


def uniNewAdmissions(request):
    if request.session.get('authenticated') == True:
        email = request.session.get('email')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT university_name FROM psapapp_uniinfotable WHERE email=%s", [email])
        uniName = cursor.fetchone()[0]
    return render(request, 'uniNewAdmissions.html', {'uniName': uniName})

# not neceessayr


def uniRegistrationForm(request):
    # Add your view logic here
    return render(request, 'uniRegistrationForm.html')


def registerasUni(request):
    if request.method == 'POST':
        d = request.POST
        email = d.get("email")
        password = d.get("password")
        university_name = d.get("university_name")
        hec_recognized = d.get("hec_recognized", "no")
        hec_registration_number = d.get("hec_registration_number")
        phone = d.get("phone")
        province = d.get("province")
        city = d.get("city")
        campus = d.get("campus")
        zip_code = d.get("zip_code")
        address = d.get("address")

        # Check if the email already exists in the database
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM psapapp_uniinfotable WHERE email=%s", [email])
        email_count = cursor.fetchone()[0]

        if email_count > 0:
            error_message = "Email is already registered to another account. Please use a different email."
            return render(request, 'uniRegistrationForm.html', {'error_message': error_message})

        else:
            # Create a new record
            c = "INSERT INTO psapapp_uniinfotable (university_name, email, password, hec_recognized, hec_registration_number, phone, province, city, campus, zip_code, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(c, [university_name, email, password, hec_recognized,
                           hec_registration_number, phone, province, city, campus, zip_code, address])

        cursor.close()

        # Redirect to the appropriate page after successful registration/update
        if 'signupasUni' in request.POST:
            return render(request, 'loginasUni.html')

    else:
        return render(request, 'registerasUni.html')


def uniUpdateForm(request):
    if request.method == 'POST':
        # Get the email and password from the form
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if the email and password match an existing record in the database
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM psapapp_uniinfotable WHERE email=%s AND password=%s", [email, password])
        email_password_match = cursor.fetchone()[0]

        if email_password_match > 0:
            # Email and password match, proceed to update the university data
            university_name = request.POST.get("university_name")
            hec_recognized = request.POST.get("hec_recognized", "no")
            hec_registration_number = request.POST.get(
                "hec_registration_number")
            phone = request.POST.get("phone")
            province = request.POST.get("province")
            city = request.POST.get("city")
            campus = request.POST.get("campus")
            zip_code = request.POST.get("zip_code")
            address = request.POST.get("address")

            # Update the record
            c = "UPDATE psapapp_uniinfotable SET university_name=%s, hec_recognized=%s, hec_registration_number=%s, phone=%s, province=%s, city=%s, campus=%s, zip_code=%s, address=%s WHERE email=%s"
            cursor.execute(c, [university_name, hec_recognized, hec_registration_number,
                           phone, province, city, campus, zip_code, address, email])
            conn.commit()

            # Redirect to the uniHome page with a success message
            success_message = "Data updated successfully!"
            return render(request, 'uniUpdateForm.html', {'success_message': success_message})

        else:
            # Email and password do not match, show an error message
            error_messageInvalidEmail = "Invalid email or password. Please try again."
            return render(request, 'uniUpdateForm.html', {'error_messageInvalidEmail': error_messageInvalidEmail})

    else:
        return render(request, 'uniUpdateForm.html')


def announce_admissions(request):
    if request.method == 'POST':
        session = request.POST.get('session')
        campus = request.POST.get('campus')
        program = request.POST.get('program')
        admission_test = request.POST.get('admission_test')
        no_of_shortlisted_students = request.POST.get(
            'no_of_shortlisted_students')
        intermediate_required_percentage = request.POST.get(
            'intermedaite_required_percentage')
        bachelor_required_percentage = request.POST.get(
            'bachelor_required_percentage')
        test_required_percentage = request.POST.get(
            'Test_required_percentage_percentage')
        departments_list = request.POST.getlist('department')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        email = request.session.get('email')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT university_name FROM psapapp_uniinfotable WHERE email=%s", [email])
        uniName = cursor.fetchone()[0]
        # Join the list of department names into a comma-separated string
        departments = ', '.join(departments_list)

        admission = Admission(
            session=session,
            campus=campus,
            program=program,
            admission_test=admission_test,
            no_of_shortlisted_students=no_of_shortlisted_students,
            intermediate_required_percentage=intermediate_required_percentage,
            bachelor_required_percentage=bachelor_required_percentage,
            test_required_percentage=test_required_percentage,
            start_date=start_date,
            end_date=end_date,
            departments=departments,
            university_name=uniName,
        )
        admission.save()

        admissions = Admission.objects.filter(university_name=uniName)
        context = {
            'admissions': admissions,
            'uniName': uniName,
        }
        return render(request, 'uniHome.html', context)

    return render(request, 'uniHome.html', {'uniName': uniName})


def university_login(request):
    if request.method == 'POST':
        cursor = conn.cursor()
        email = request.POST['email']
        password = request.POST['password']
        c = "SELECT * FROM psapapp_uniinfotable WHERE email='{}' AND password='{}'".format(
            email, password)
        cursor.execute(c)
        authenticated = tuple(cursor.fetchall())
        if authenticated:
            request.session['authenticated'] = True
            request.session['email'] = email
            cursor.execute(
                "SELECT university_name from psapapp_uniinfotable WHERE email=%s", [email])
            uniName = cursor.fetchone()[0]
            admissions = Admission.objects.filter(university_name=uniName)
            context = {
                'admissions': admissions,
                'uniName': uniName,
            }
            return render(request, 'uniHome.html', context)
        else:
            messages.error(request, 'Invalid Email or Password')
            return render(request, 'loginasUni.html')
    else:
        logout(request)
        return render(request, 'loginasUni.html')


# Student Work


def student_registration(request):
    if request.method == 'POST':
        d = request.POST
        first_name = d.get("first_name")
        last_name = d.get("last_name")
        dob = d.get("dob")
        cnic = d.get("cnic")
        gender = d.get("gender")
        email = d.get("email")
        password = d.get("password")
        phone = d.get("phone")
        province = d.get("province")
        city = d.get("city")
        zip_code = d.get("zip_code")
        address = d.get("address")
        intermediate = d.get("intermediate")
        college_name = d.get("college_name")
        college_graduation_date = d.get("college_graduation_date")
        inter_obtained_marks = d.get("inter_obtained_marks", 0)
        inter_total_marks = d.get("inter_total_marks", 0)
        matriculation = d.get("matriculation")
        school_name = d.get("school_name")
        matric_graduation_date = d.get("matric_graduation_date")
        matric_obtained_marks = d.get("matric_obtained_marks", 0)
        matric_total_marks = d.get("matric_total_marks", 0)
        # document
        self_photo = request.FILES['self_photo']
        id_card_photo = request.FILES['id_card_photo']
        inter_transcript = request.FILES['inter_transcript']
        inter_degree = request.FILES['inter_degree']
        matric_transcript = request.FILES['matric_transcript']
        matric_degree = request.FILES['matric_degree']

        # Check if the email already exists in the database
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM psapapp_stdinfotable WHERE email=%s", [email])
        email_count = cursor.fetchone()[0]

        if email_count > 0:
            error_message = "Email is already registered to another account. Please use a different email."
            return render(request, 'registerasStd.html', {'error_message': error_message})

        else:
            # Create a new student record
            # password_hashed = make_password(password)
            c = "INSERT INTO psapapp_stdinfotable (first_name, last_name, dob, cnic, gender, email, password, phone, province, city, zip_code, address, intermediate, college_name, college_graduation_date, inter_obtained_marks, inter_total_marks, matriculation, school_name, matric_graduation_date, matric_obtained_marks, matric_total_marks, self_photo, id_card_photo, inter_transcript, inter_degree, matric_transcript, matric_degree) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            cursor.execute(c, [first_name, last_name, dob, cnic, gender, email, password, phone, province, city, zip_code, address, intermediate, college_name,
                               college_graduation_date, inter_obtained_marks, inter_total_marks, matriculation, school_name, matric_graduation_date, matric_obtained_marks, matric_total_marks, self_photo, id_card_photo, inter_transcript, inter_degree, matric_transcript, matric_degree])

            cursor.close()

        # Redirect to the appropriate page after successful registration/update
        if 'signupasStd' in request.POST:
            return render(request, 'loginasStd.html')
        success_message = "Account created successfully! Please login"
        return render(request, 'registerasStd.html', {'success_message': success_message})

    else:
        return render(request, 'registerasUni.html')


def student_login(request):
    if request.method == 'POST':
        cursor = conn.cursor()
        email = request.POST['email']
        password = request.POST['password']
        c = "SELECT * FROM psapapp_stdinfotable WHERE email='{}' AND password='{}'".format(
            email, password)
        cursor.execute(c)
        authenticated = tuple(cursor.fetchall())
        if authenticated:
            request.session['authenticated'] = True
            request.session['email'] = email

            # cursor.execute(
            #     "SELECT email from psapapp_stdinfotable WHERE email=%s", [email])
            # email = cursor.fetchone()[0]
            cursor.execute(
                "SELECT first_name from psapapp_stdinfotable WHERE email=%s", [email])
            stdName = cursor.fetchone()[0]
            return render(request, 'stdHome.html', {'stdName': stdName})
        else:
            messages.error(request, 'Invalid Email or Password')
            return render(request, 'loginasStd.html')
    else:
        logout(request)
        return render(request, 'loginasStd.html')


def stdUpdateForm(request):
    if request.method == 'POST':
        # Get the email and password from the form
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if the email and password match an existing record in the database
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM psapapp_stdinfotable WHERE email=%s AND password=%s", [email, password])
        email_password_match = cursor.fetchone()[0]

        if email_password_match > 0:
            # Email and password match, proceed to update the student data
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            dob = request.POST.get("dob")
            cnic = request.POST.get("cnic")
            gender = request.POST.get("gender")
            phone = request.POST.get("phone")
            province = request.POST.get("province")
            city = request.POST.get("city")
            zip_code = request.POST.get("zip_code")
            address = request.POST.get("address")
            intermediate = request.POST.get("intermediate")
            college_name = request.POST.get("college_name")
            college_graduation_date = request.POST.get(
                "college_graduation_date")
            inter_obtained_marks = request.POST.get("inter_obtained_marks")
            inter_total_marks = request.POST.get("inter_total_marks")
            matriculation = request.POST.get("matriculation")
            school_name = request.POST.get("school_name")
            matric_graduation_date = request.POST.get("matric_graduation_date")
            matric_obtained_marks = request.POST.get("matric_obtained_marks")
            matric_total_marks = request.POST.get("matric_total_marks")

            # Update the record
            update_query = """
                    UPDATE psapapp_stdinfotable 
                    SET first_name = %s, last_name = %s, dob = %s, cnic = %s, gender = %s, 
                    phone = %s, province = %s, city = %s, zip_code = %s, address = %s, 
                    intermediate = %s, college_name = %s, college_graduation_date = %s, 
                    inter_obtained_marks = %s, inter_total_marks = %s, matriculation = %s, 
                    school_name = %s, matric_graduation_date = %s, matric_obtained_marks = %s, 
                    matric_total_marks = %s 
                    WHERE email = %s AND password = %s
                """

            # Execute the query
            cursor.execute(update_query, (first_name, last_name, dob, cnic, gender, phone,
                                          province, city, zip_code, address, intermediate,
                                          college_name, college_graduation_date,
                                          inter_obtained_marks, inter_total_marks,
                                          matriculation, school_name, matric_graduation_date,
                                          matric_obtained_marks, matric_total_marks,
                                          email, password))

            # Commit the changes to the database
            conn.commit()

            # Redirect to the update form page with a success message
            success_message = "Data updated successfully!"
            return render(request, 'stdUpdate.html', {'success_message': success_message},)

        else:
            # Email and password do not match, show an error message
            error_message = "Invalid email or password. Please try again."
            return render(request, 'stdUpdate.html', {'error_message': error_message},)

    else:
        return render(request, 'stdUpdate.html')


def apply_admission(request):
    if request.session.get('authenticated') == True:
        email = request.session.get('email')
        # Get the selected university from the form data
        selected_university = request.POST.get('university')

        # Check if a university is selected
        if selected_university:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT university_name FROM psapapp_uniinfotable WHERE email=%s AND university_name=%s",
                [email, selected_university]
            )
            university_name = cursor.fetchone()

            if university_name:
                return render(request, 'uniHome.html', {'email': email, 'university': university_name})
            else:
                return render(request, 'uniHome.html', {'message': 'University not found for the given email.'})
        else:
            return render(request, 'uniHome.html', {'message': 'Please select a university.'})
    else:
        return render(request, 'stdHome.html', {'message': 'User not authenticated.'})
