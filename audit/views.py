from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .models import AccessLog, ChangeLog, System
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime

def dashboard(request):
    systems = System.objects.all()
    access_logs = AccessLog.objects.order_by('-timestamp')[:10]
    change_logs = ChangeLog.objects.order_by('-timestamp')[:10]
    
    context = {
        'systems': systems,
        'access_logs': access_logs,
        'change_logs': change_logs,
        'total_systems': systems.count(),
    }
    return render(request, 'dashboard.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        # Get client IP address
        ip_address = get_client_ip(request)
        
        if user is not None:
            # Log SUCCESSFUL login
            AccessLog.objects.create(
                user=user,
                event_type='LOGIN_SUCCESS',
                ip_address=ip_address,
                details=f'Successful login from IP: {ip_address}'
            )
            
            login(request, user)
            messages.success(request, f'Welcome {username}!')
            return redirect('dashboard')
        else:
            # Log FAILED login attempt
            AccessLog.objects.create(
                user=None,  # No user for failed attempts
                event_type='LOGIN_FAIL',
                ip_address=ip_address,
                details=f'Failed login attempt for username: {username} from IP: {ip_address}'
            )
            
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

def user_logout(request):
    if request.user.is_authenticated:
        # Log logout event
        AccessLog.objects.create(
            user=request.user,
            event_type='LOGOUT',
            ip_address=get_client_ip(request),
            details='User logged out successfully'
        )
    
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

def generate_compliance_report(request):
    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()
    
    # Create the PDF object
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Add title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center aligned
    )
    story.append(Paragraph("ITGC COMPLIANCE REPORT", title_style))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Add Systems Summary
    story.append(Paragraph("Systems Being Audited", styles['Heading2']))
    systems = System.objects.all()
    systems_data = [['System Name', 'Description']]
    for system in systems:
        systems_data.append([system.name, system.description])
    
    systems_table = Table(systems_data)
    systems_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(systems_table)
    story.append(Spacer(1, 20))
    
    # Add Access Logs Summary
    story.append(Paragraph("Recent Access Events", styles['Heading2']))
    access_logs = AccessLog.objects.order_by('-timestamp')[:20]
    access_data = [['Timestamp', 'User', 'Event Type', 'IP Address']]
    for log in access_logs:
        access_data.append([
            log.timestamp.strftime('%Y-%m-%d %H:%M'),
            str(log.user) if log.user else 'N/A',
            log.get_event_type_display(),
            log.ip_address or 'N/A'
        ])
    
    access_table = Table(access_data)
    access_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8)
    ]))
    story.append(access_table)
    story.append(Spacer(1, 20))
    
    # Build PDF
    doc.build(story)
    
    # Get PDF value from buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    # Create HTTP response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="itgc_compliance_report.pdf"'
    response.write(pdf)
    return response

# Helper function to get client IP address
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip