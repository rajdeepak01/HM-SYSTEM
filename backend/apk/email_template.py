from jinja2 import Template


def render_email_template(username, appointments):

    template = Template("""

    <h2>Monthly Activity Report</h2>

    <p>Hello {{username}},</p>

    <p>Here is your monthly report.</p>

    <table border="1">

    <tr>
        <th>Date</th>
        <th>Patient</th>
        <th>Status</th>
    </tr>

    {% for a in appointments %}

    <tr>
        <td>{{a.date}}</td>
        <td>{{a.patient.patientName}}</td>
        <td>{{a.status}}</td>
    </tr>

    {% endfor %}

    </table>

    """)

    return template.render(username=username, appointments=appointments)