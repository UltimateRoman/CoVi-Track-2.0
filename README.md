# CoVi-Track

### CS50x 2020 Final Project by Athul Sanjose

CoVi-Track is a Web-App built using Flask, HTML, CSS with a SQL database.
It mainly serves the purposes of CoViD-19 statistics tracking and symptoms monitoring for individuals. It also displays and endorses precautions
against CoViD-19 with a purpose of spreading awareness among its users.

## Statistics Tracking

  CoVi-Track can access and display data about CoViD-19 cases. This includes country-specific, American and Indian states-specific statistics.
Data available include the total number of cases, active cases, recovered cases, deaths, number of tests among others. Users can easily search and view
the statistics of any location of their choice from among these three groups.
This data is sourced from worldometers.info through the Novel COVID API.

## Symptoms Monitoring

  A user can create an account on CoVi-Track with a suitable username and password. On a daily-basis, he/she is prompted to complete a simple checkbox
form to identify the symptoms they experience, if any. Based on this, the Web-App allots them risk points. The lower their current risk points, the safer
they are currently. The corresponding points are assigned based on the severity and uniqueness of the symptoms with that of CoViD-19. This helps the
users to easily identify their risk levels. A history of the user's daily risk point statistics is also available so that the user will have a record
of their symptoms' variation over time.

   But this mechanism is quite facile because it follows a symptom-based model of diagnosis and cannot guarantee cent percent success because the nature
of the disease is such that many cases are asymptomatic and testing is required for confirmation. So CoVi-Track can actually complement testing by
identifying appropriate individuals for testing thus improving efficiency of testing efforts by the government for identification and treatment of
CoViD-19 infected patients.