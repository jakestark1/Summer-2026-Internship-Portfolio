from IPython.display import display, HTML
from bs4 import BeautifulSoup
import base64
import re

# Original HTML content definition
html_content = """<!DOCTYPE html>
<html lang=\"en\">
<head>
<meta charset=\"UTF-8\">
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
<title>[Jake Stark] - Internship Portfolio</title>
<style>
  :root{
    --ink:#1B2430;
    --paper:#F7F5F0;
    --paper-dim:#EFEBE2;
    --clay:#C8714A;
    --sage:#6E8268;
    --line:#D8D2C4;
    --text:#23262C;
    --text-soft:#5B5E63;
  }
  *{box-sizing:border-box;}
  html{scroll-behavior:smooth;}
  body{
    margin:0;
    background:var(--paper);
    color:var(--text);
    font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;
    line_height:1.55;
  }
  @media (prefers-reduced-motion: reduce){
    *{animation-duration:0.01ms !important; transition-duration:0.01ms !important;}
  }
  h1,h2,h3{
    font-family:'Fraunces','Georgia',serif;
    font-weight:600;
    margin:0;
    color:var(--ink);
  }
  .mono{
    font-family:'IBM Plex Mono','Courier New',monospace;
    letter-spacing:.03em;
  }
  a{color:inherit;}
  .wrap{max-width:920px; margin:0 auto; padding:0 28px;}

  /* ---------- INSTRUCTIONS BANNER (delete before publishing) ---------- */
  .howto{
    background:#2B3340;
    color:#D8DDE3;
    font-family:'IBM Plex Mono',monospace;
    font-size:13px;
    padding:14px 28px;
    border-bottom:2px dashed var(--clay);
  }
  .howto b{color:#fff;}

  /* ---------- NAV ---------- */
  nav{
    position:sticky; top:0; z-index:50;
    background:rgba(247,245,240,0.92);
    backdrop-filter:blur(6px);
    border-bottom:1px solid var(--line);
  }
  nav .wrap{display:flex; align-items:center; justify-content:space-between; padding:14px 28px;}
  .nav-name{font-family:'Fraunces',serif; font-weight:600; font-size:18px;}
  .nav-links{display:flex; gap:24px; font-size:13px;}
  .nav-links a{
    text-decoration:none; color:var(--text-soft);
    text-transform:uppercase; letter-spacing:.08em; font-family:'IBM Plex Mono',monospace;
    font-size:11px;
    border-bottom:1px solid transparent;
    padding-bottom:2px;
  }
  .nav-links a:hover{color:var(--clay); border-bottom-color:var(--clay);}

  /* ---------- HERO ---------- */
  header.hero{padding:90px 0 70px; border-bottom:1px solid var(--line); position:relative;}
  .eyebrow{
    font-family:'IBM Plex Mono',monospace;
    font-size:12px;
    color:var(--clay);
    text-transform:uppercase;
    letter-spacing:.12em;
    margin-bottom:18px;
    display:flex; align-items:center; gap:10px;
  }
  .eyebrow::before{content:\"\"; width:24px; height:1px; background:var(--clay); display:inline-block;}
  .hero h1{font-size:54px; line_height:1.05; max-width:680px;}
  .hero .role{font-size:22px; color:var(--text-soft); margin-top:14px; font-family:'Fraunces',serif; font-style:italic;}
  .hero-meta{
    display:flex; gap:32px; margin-top:36px; flex-wrap:wrap;
  }
  .hero-meta div{font-family:'IBM Plex Mono',monospace; font-size:12px; color:var(--text-soft);}
  .hero-meta div span{display:block; color:var(--ink); font-size:14px; margin-top:4px;}

  /* ---------- SECTION SHELL ---------- */
  section{padding:64px 0; border-bottom:1px solid var(--line);}
  .section-head{display:flex; align-items:baseline; gap:16px; margin-bottom:40px;}
  .section-num{font-family:'IBM Plex Mono',monospace; color:var(--clay); font-size:13px;}
  .section-head h2{font-size:30px;}

  /* ---------- ABOUT ---------- */
  .about-grid{display:grid; grid-template-columns:1.3fr 1fr; gap:48px;}
  .about-grid p{color:var(--ink); max-width:520px;}
  .field-notes{
    background:var(--paper-dim);
    border-left:3px solid var(--sage);
    padding:18px 20px;
    font-size:15px;
  }
  .field-notes .mono{font-size:11px; color:var(--sage); text-transform:uppercase; display:block; margin-bottom:8px;}

  /* ---------- METRICS / IMPACT ---------- */
  .metrics{display:grid; grid-template-columns:repeat(3,1fr); gap:1px; background:var(--line); border:1px solid var(--line);}
  .metric{background:var(--paper); padding:28px 24px; text-align:center;}
  .metric .num{font-family:'Fraunces',serif; font-size:40px; color:var(--clay); line_height:1;}
  .metric .label{font-size:13px; color:var(--text-soft); margin-top:8px;}

  /* ---------- PROJECT LOG ---------- */
  .entry{
    display:grid; grid-template-columns:140px 1fr; gap:32px;
    padding:32px 0; border-top:1px solid var(--line);
  }
  .entry:first-of-type{border-top:none;}
  .entry-date{font-family:'IBM Plex Mono',monospace; font-size:12px; color:var(--text-soft); padding-top:4px;}
  .entry-date .week{display:block; color:var(--ink); font-size:13px; margin-bottom:4px;}
  .stamp{
    display:inline-block;
    margin-top:14px;
    font-family:'IBM Plex Mono',monospace;
    font-size:10px;
    text-transform:uppercase;
    letter-spacing:.08em;
    color:var(--sage);
    border:1.5px solid var(--sage);
    padding:3px 8px;
    transform:rotate(-2deg);
    border-radius:2px;
  }
  .entry h3{font-size:21px; margin-bottom:8px;}
  .entry p{color:var(--text-soft); margin:0 0 12px;}
  .tags{display:flex; gap:8px; flex-wrap:wrap; margin-top:14px;}
  .tag{
    font-family:'IBM Plex Mono',monospace;
    font-size:11px;
    background:var(--paper-dim);
    color:var(--text-soft);
    padding:4px 10px;
    border-radius:12px;
  }

  /* ---------- SKILLS ---------- */
  .skills-list{display:flex; flex-wrap:wrap; gap:10px;}
  .skill-pill{
    border:1px solid var(--ink);
    color:var(--ink);
    font-family:'IBM Plex Mono',monospace;
    font-size:12px;
    padding:6px 14px;
    border-radius:20px;
  }

  /* ---------- REFLECTION ---------- */
  .reflection-quote{
    font-family:'Fraunces',serif;
    font-style:italic;
    font-size:24px;
    line_height:1.4;
    color:var(--ink);
    max-width:680px;
    border-left:3px solid var(--clay);
    padding-left:24px;
  }
  .reflection-quote span{display:block; font-family:'IBM Plex Mono',monospace; font-style:normal; font-size:12px; color:var(--text-soft); margin-top:16px;}

  /* ---------- ABOUT ME ---------- */
  .about-me-grid{
    display:grid;
    grid-template-columns:270px 1fr;
    gap:30px;
    align-items:start;
    justify-items:start;
  }
  .about-me-photo img{
    width:100%;
    aspect-ratio:1/1;
    object-fit:cover;
    border-radius:4px;
    border:1px solid var(--line);
    margin-top:8px;
  }
  .about-me-photo{
    margin:0;
    padding:0;
  }
  .about-me-text p{
    color:var(--ink);
    max-width:560px;
  }
    #about-me .section-head{
    margin-bottom:20px;
  }

   /* ---------- CONTACT / FOOTER ---------- */
  footer{padding:70px 0 90px;}
  footer h2{font-size:32px; margin-bottom:18px;}
  .contact-row{display:flex; gap:28px; flex-wrap:wrap; margin-top:22px;}
  .contact-row a{
    border:1px solid var(--line);
    font-family:'IBM Plex Mono',monospace;
    font-size:14px;
    text-decoration:none;
    padding-bottom:2px;
    color:var(--ink);
    border-radius:20px;
  }
  .contact-row a:hover{color:var(--clay);}

  .contact-cards{
    display:grid;
    grid-template-columns:repeat(3, 1fr);
    gap:1px;
    background:var(--line);
    border:1px solid var(--line);
  }
  .contact-card{
    background:var(--paper);
    padding:24px 20px;
    text-decoration:none;
    display:flex;
    flex-direction:column;
    gap:6px;
    transition:background .15s ease;
  }
  .contact-card:hover{
    background:var(--paper-dim);
  }
  .contact-label{
    font-family:'IBM Plex Mono',monospace;
    font-size:12px;
    text-transform:uppercase;
    letter-spacing:.08em;
    color:var(--clay);
     font-weight:700;
  }
  .contact-value{
    font-size:14px;
    color:var(--ink);
    word-break:break-word;
  }
  #contact .section-head{
    padding-left:0;
    margin-left:0;
  }
  @media (max-width:720px){
    .about-me-grid{grid-template-columns:1fr;}
    .hero h1{font-size:36px;}
    .about-grid{grid-template-columns:1fr;}
    .metrics{grid-template-columns:1fr;}
    .entry{grid-template-columns:1fr;}
    .nav-links{display:none;}
    .contact-cards{grid-template-columns:1fr;}
  }
</style>
</head>
<body>

<nav>
  <div class=\"wrap\">
    <div class=\"nav-name\">Jake Stark &ndash; Business Operations Intern </div>
    <div class=\"nav-links\">
      <a href=\"#about\">About</a>
      <a href=\"#impact\">Impact</a>
      <a href=\"#log\">Project Log</a>
      <a href=\"#skills\">Skills</a>
      <a href=\"#reflection\">Reflection</a>
      <a href=\"#about me\">About Me</a>
      <a href=\"#contact\">Contact</a>
    </div>
  </div>
</nav>

<header class=\"hero\">
  <div class=\"wrap\">
    <div class=\"eyebrow\">Internship Portfolio &middot; Summer 2026</div>
    <h1>Jake Stark</h1>
    <div class=\"role\" style=\"color:var(--text-soft); font-weight: bold;\">Business Operations Intern at The Arc of Essex County</div>
    <div class=\"hero-meta\">
      <div><span style="color:#C8714A;">DURATION</span> <span>10 Weeks: June–August</span></div>
      <div><span style="color:#C8714A;">DEPARTMENT</span> <span>Human Resources/Finance</span></div>
      <div><span style="color:#C8714A;">FOCUS</span> <span>Interdepartmental Operations</span></div>
    </div>
  </div>
</header>

<section id=\"about\">
  <div class=\"wrap about-grid\">
    <div>
      <div class=\"section-head\">
        <h2>About this Internship</h2>
      </div>
      <p>The Arc of Essex County is a nonprofit agency founded in 1948 with a mission to provide advocacy and services empowering individuals with intellectual and developmental disabilities and their families. It is the largest chapter of The Arc in New Jersey, working with a budget of over $39 million and serving over 1,500 individuals across more than 40 programs and services.
      <p>As a Business Operations Intern, I have specialized in the processes supporting daily operations with the Human Resources and Finance departments. Through this role, I have gained real experience managing the agency's workflow and recruitment efforts, auditing files to assure complaince, streamlining cross-department operations, and managing projects to increase efficiency by implementing new data systems.
    </div>
    <div class=\"field-notes\" style=\"text-align:center;\">
  <img
    src=\"Arc Essex Logo.png\"
    alt=\"The Arc of Essex County Logo\"
    style=\"max-width:300px;\"
  >
</div>
  </div>
</section>

<section id=\"impact\">
  <div class=\"wrap\">
    <div class=\"section-head\">
      <h2>Impact by the Numbers</h2>
    </div>
    <div class=\"metrics\">
      <div class=\"metric\">
        <div class=\"num\">500+</div>
        <div class=\"label\">Documents and profiles reviewed, organized, and uploaded</div>
      </div>
      <div class=\"metric\">
        <div class=\"num\">3</div>
        <div class=\"label\">Stepping Stones Teacher's Assistants hired</div>
      </div>
      <div class=\"metric\">
        <div class=\"num\">200</div>
        <div class=\"label\">Hours spent developing data systems, screening employment applicants, and improving operations processes</div>
      </div>
    </div>
  </div>
</section>

<section id=\"log\">
  <div class=\"wrap\">
    <div class=\"section-head\">
      <h2>Project Log</h2>
    </div>

    <!-- Duplicate this .entry block for each project -->
    <div class=\"entry\">
      <div class=\"entry-date\">
        <span class=\"week\">Weeks 1–3</span>
        [Jun 1 – Jun 19]
      </div>
      <div>
        <h3>Job Description Compliance Audit</h3>
        <p><span style=\"color: #C8714A; font-weight: bold;\">Search internal files to identify potential issues regarding compliance<span></p>
        <p>With this project, I conducted an audit of the agency's active job descriptions, identifying any that may fail to comply with agency standards along with any active positions in our staff pattern that lacked a corresponding job description. I took notes of any discrepancies in formatting or information included, as well as outdated files. From there, I searched employee profiles through our HRIS to identify those lacking a signed job description or a matching title. All findings were documented in an Excel spreasdsheet where I analyzed the data and presented my actions steps to the Director of Recruitment, Onboarding, and Employee Engagement and the Manager of Recruitment.</p>
        <p><span style=\"color: #C8714A; font-weight: bold;\">Results:</span> My findings and action steps were later presented to our Chief Administrative Officer who coordinated action to resolve any errors and assure compliance with Medicaid and the NJ Department of Developmental Disabilities standards.</p>
        <div class=\"tags\">
          <span class=\"tag\">[Spreadsheet Modeling]</span>
          <span class=\"tag\">[Departmental Compliance]</span>
          <span class=\"tag\">[Internal Auditing]</span>
        </div>
        <span class=\"stamp\">Completed</span>
      </div>
    </div>

    <div class=\"entry\">
      <div class=\"entry-date\">
        <span class=\"week\">Weeks 2–6</span>
        [Jun 8 – Jul 17]
      </div>
      <div>
        <h3>Teacher's Assistant Applicant Hiring</h3>
        <p><span style=\"color: #C8714A; font-weight: bold;\">Facilitate the hiring of three new teacher's assistants for the Stepping Stones School<span></n>
        <p>Through this project, I took part in the hiring process for teacher's assistants at the Stepping Stones School. This ranged from initial application screening through the applicant tracking system, to extending a job offer for hired applicants. I screened over 50 applications and resumes, conducting phone screenings to those deemed fit. For strong applicants, I scheduled interviews with the Stepping Stones School administrators and sent email confirmations to applicants with interview details. If chosen to be hired, I took part in extending an official offer to complete the first phase of the hiring process.</n>
        <p><span style=\"color: #C8714A; font-weight: bold;\">Results:</span> Three Teacher's Assistants that I screened were hired and sent for new employee onboarding.</n>
        <div class=\"tags\">
          <span class=\"tag\">[Applicant Tracking System]</span>
          <span class=\"tag\">[Resume Screening]</span>
          <span class=\"tag\">[Cross-Department Collaboration]</span>
        </div>
        <span class=\"stamp\">Completed</span>
      </div>
    </div>

    <div class=\"entry\">
      <div class=\"entry-date\">
        <span class=\"week\">Weeks 2–5</span>
        [Jun 8 – Jul 2]
      </div>
      <div>
        <h3>Employee Engagement and Appreciation</h3>
        <p><span style=\"color: #C8714A; font-weight: bold;\">Develop, pitch, and implement initiatives for employee engagement and DSP Appreciation Week<span></n>
        <p>With the Engagement Team, I researched and discussed initiatives for our DSP Appreciation Week, as well as general agency engagement strategies. We looked into former initiatives and established potential changes that can be made for greater impact. Additionally, we discussed ways to improve organizational culture and employee motivation, including increasing participation in our Arc Hero recognition program.</n>
        <p><span style=\"color: #C8714A; font-weight: bold;\">Results:</span> These ideas were pitched to the Chief Administrative Officer and received approvals. These initiatives will continue to be implemented over the coming months.</n>
        <div class=\"tags\">
          <span class=\"tag\">[Employee Engagement]</span>
          <span class=\"tag\">[Process Implementation]</span>
          <span class=\"tag\">[Organizational Culture]</span>
        </div>
        <span class=\"stamp\">In progress</span>
      </div>
    </div>

    <div class=\"entry\">
      <div class=\"entry-date\">
        <span class=\"week\">Week 4</span>
        [Jun 22 - Jun 26]
      </div>
      <div>
        <h3>Local Business Sponsorships</h3>
        <p><span style=\"color: #C8714A; font-weight: bold;\">Work with local businesses to secure sponsorships for our Uncorked and Uncapped fundraiser</n>
        <p>Working with the marketing department, I met with the owner of Stella, a local restaurant, to inquire about having them be a sponsor for our Uncorked and Uncapped fundraiser this fall. As part of this fundraiser, we are looking for local restaurants to give out food samples which will increase event attendance and allow restaurants to advertise.</n>
        <p><span style=\"color: #C8714A; font-weight: bold;\">Results:</span> The owner of the restaurant agreed to the sponsorship and will take part in our fundraiser in October.</n>
        <div class=\"tags\">
          <span class=\"tag\">[Business Partnerships]</span>
          <span class=\"tag\">[Event Planning]</span>
          <span class=\"tag\">[Marketing & Advertising]</span>
        </div>
        <span class=\"stamp\">Completed</span>
      </div>
    </div>

    <div class=\"entry\">
      <div class=\"entry-date\">
        <span class=\"week\">Weeks 4-10</span>
        [Jun 22 - Aug 12]
      </div>
      <div>
        <h3>Internship Portfolio</h3>
        <p><span style=\"color: #C8714A; font-weight: bold;\">Create a portfolio to display my internship projects and experiences</n>
        <p>Throughout my time as an intern, I have worked to code and develop this portfolio to display my experiences and projects from the internship program. The original template for the portfolio was coded to my desires using Claude AI. I then converted and pasted the code into Google Colab where I have continuously made edits to personalize the portfolio with my own information and formatting.</n>
        <p><span style=\"color: #C8714A; font-weight: bold;\">Results:</span> This portfolio will be used to display my work as an intern for my own professional development. Additionally, it will be utilized by The Arc of Essex County to develop the internship program. It will also be sent to the Office of the Secretary of Higher Education (OSHE) to display how the agency utilizes its interns and to help plead for more grant funding for future interns.</n>
        <div class=\"tags\">
          <span class=\"tag\">[Web Design]</span>
          <span class=\"tag\">[AI Coding]</span>
          <span class=\"tag\">[Personal Brand Management]</span>
        </div>
        <span class=\"stamp\">Completed</span>
      </div>
    </div>

  <div class=\"entry\">
      <div class=\"entry-date\">
        <span class=\"week\">Weeks 4-8</span>
        [Jun 22 - Jul 30]
      </div>
      <div>
        <h3>Intern Job Descriptions</h3>
        <p><span style=\"color: #C8714A; font-weight: bold;\">Create an official job description for all agency internship positions</n>
        <p>Following up on my job description compliance audit, I created official job descriptions to be used for the Business Operations Intern and the Recreation & Leisure Intern positions. The job descriptions have been tailored to comply with departmental standards. This will be used to further develop the internship program, and it will be signed by all future Business Operations and Recreation & Leisure Interns.</n>
        <p><span style=\"color: #C8714A; font-weight: bold;\">Results:</span> These job descriptions have been sent to the agency's Chief Executive Officer for approval.</n>
        <div class=\"tags\">
          <span class=\"tag\">[Departmental Compliance]</span>
          <span class=\"tag\">[Professional Writing]</span>
          <span class=\"tag\">[Internship Program Development]</span>
        </div>
        <span class=\"stamp\">Completed</span>
      </div>
    </div>

  <div class=\"entry\">
      <div class=\"entry-date\">
        <span class=\"week\">Week 5</span>
        [Jun 29 - Jul 2]
      </div>
      <div>
        <h3>Q2 Transfer Data Report</h3>
        <p><span style=\"color: #C8714A; font-weight: bold;\">Create a report displaying transfer data and trends from 2026 Q2</n>
        <p>To assist our Assistant Director of Recruitment, I analyzed raw data from agency transfers throughout the second quarter of the calendar year. I focused on departmental transfers, promotions, and schedule changes in order to identify trends with staff pattern changes. I then created a report with my findings, which made the data concise and understandable.</n>
        <p><span style=\"color: #C8714A; font-weight: bold;\">Results:</span>  My report was used by the Assistant Director of Recruitment as part of his quarterly report, which was presented to the agency's administrative board.</n>
        <div class=\"tags\">
          <span class=\"tag\">[Data Analysis]</span>
          <span class=\"tag\">[Trend Identification]</span>
          <span class=\"tag\">[Quartely Reporting]</span>
        </div>
        <span class=\"stamp\">Completed</span>
      </div>
    </div>

      <div class=\"entry\">
      <div class=\"entry-date\">
        <span class=\"week\">Weeks 6-7</span>
        [Jul 13 - Jul 24]
      </div>
      <div>
        <h3>Consumer File Audit</h3>
        <p><span style=\"color: #C8714A; font-weight: bold;\">Audit, upload, and organize consumer files to track important documentation</n>
        <p>To prepare the agency for audits and to ensure all necessary consumer documents are uploaded, I tracked consumer housing renewal forms and acuity forms. All forms were tracked with an Excel spreadsheet to flag issues. Files were downloaded and moved to folders, then uploaded to an agency database for easy access.</n>
        <p><span style=\"color: #C8714A; font-weight: bold;\">Results:</span> Nearly 200 consumer files were tracked, moved to folders, and uploaded to an agency database.</n>
        <div class=\"tags\">
          <span class=\"tag\">[Internal Auditing]</span>
          <span class=\"tag\">[Medicare & Medicaid Compliance]</span>
          <span class=\"tag\">[Data Entry]</span>
        </div>
        <span class=\"stamp\">Completed</span>
      </div>
    </div>

      <div class=\"entry\">
      <div class=\"entry-date\">
        <span class=\"week\">Weeks 7-10</span>
        [Jul 20 - Aug 12]
      </div>
      <div>
        <h3>Attendance Point Tracking System</h3>
        <p><span style=\"color: #C8714A; font-weight: bold;\">Manage a project to create and implement a more efficient attendance point tracking system</n>
        <p>For this project, I have managed the development of a new system used to track discipline points awarded for attendance violations. This system will serve as a central database for attendance point tracking and will include automated reports with data linked to agency timesheets. Working with the Finance and HR departments, I have led the organization of project documentation, prepared meeting agendas and materials, and researched system configurations that could be implemented.</n>
        <p><span style=\"color: #C8714A; font-weight: bold;\">Results:</span> The plan of approach and guidelines that I have set for this project will be continued to be used as the system is developed throughout the next few months.</n>
        <div class=\"tags\">
          <span class=\"tag\">[System Design]</span>
          <span class=\"tag\">[Project Management]</span>
          <span class=\"tag\">[Meeting Facilitation]</span>
        </div>
        <span class=\"stamp\">In Progress</span>
      </div>
    </div>

      <div class=\"entry\">
      <div class=\"entry-date\">
        <span class=\"week\">Weeks 7-10</span>
        [Jul 20 - Aug 12]
      </div>
      <div>
        <h3>ISP Renewal Tracking System</h3>
        <p><span style=\"color: #C8714A; font-weight: bold;\">Work with a team to create an AI powered tracking system for ISP renewal schedules</n>
        <p>All consumers of The Arc have Individual Support Plans, which are required to be renewed each year. To improve efficiency for this process, I have been working on a team to track the ISP renewal process and create an Azure AI powered system to automate renewal tracking. The system is being programmed to extract information from ISP forms, upload data to a shared database, and automate notifications for upcoming deadlines.</n>
        <p><span style=\"color: #C8714A; font-weight: bold;\">Results:</span> The system is currently being designed with my guidance and will continue to be configured and implemented in the coming months.</n>
        <div class=\"tags\">
          <span class=\"tag\">[AI Implementation]</span>
          <span class=\"tag\">[System Design]</span>
          <span class=\"tag\">[Power Automations]</span>
        </div>
        <span class=\"stamp\">In Progress</span>
      </div>
    </div>

  </div>
</section>

<section id=\"skills\">
  <div class=\"wrap\">
    <div class=\"section-head\">
      <h2>Skills Developed</h2>
    </div>
    <div class=\"skills-list\">
      <span class=\"skill-pill\">Project Management</span>
      <span class=\"skill-pill\">Data System Development</span>
      <span class=\"skill-pill\">Personnel Recruitment</span>
      <span class=\"skill-pill\">Data Analysis</span>
      <span class=\"skill-pill\">Compliance Assurance</span>
      <span class=\"skill-pill\">Professionalism</span>
      <span class=\"skill-pill\">Workplace Communication</span>
      <span class=\"skill-pill\">Meeting Facilitation</span>
      <span class=\"skill-pill\">Appropriate AI Use</span>
      <span class=\"skill-pill\">Spreadsheet Modeling</span>
    </div>
  </div>
</section>

<section id=\"reflection\">
  <div class=\"wrap\">
    <div class=\"section-head\">
      <h2>Reflection</h2>
    </div>
    <div class=\"reflection-quote\">
      \"My time interning at The Arc of Essex County has been more impactful than I could have ever imagined. Everybody I have worked with has been an amazing mentor and they have done so much for my own professional development. The HR and Finance departments were patient with me throughout the whole process and always found ways to keep me involved. I was introduced to projects designed around my interests and given the opportunity to lead my own initiatives. Although I am sad that this internship is coming to an end, I’m incredibly grateful for this opportunity. Without a doubt, interning at The Arc of Essex County has prepared me for a successful career in business!\"
    </div>
  </div>
</section>

<section id="about-me">
  <div class="wrap">
    <div class="section-head">
      <h2>About Me</h2>
    </div>
    <div class="about-me-grid">
  <div class="about-me-photo">
    <div class="photo-frame">
      <img src="Professional Headshot.jpg" alt="Jake Stark">
    </div>
  </div>
  <div class="about-me-text">
    <p>
      Hey! My name is Jake Stark, and I am entering my junior year at the University of Connecticut. I am currently pursuing a degree in Business Management, with a minor in Analytics. I have strong passions for growth strategy, organizational development, data analysis, and organizational behavior. I am currently looking to pursue a career in Management Consulting, Corporate Strategy, or Business Process Management, but I am open to many different career paths.
    </p>
    <p>
      Over the past few years, I've been part of various organizations and have held many leadership positions that have helped me develop my skillset. At the University of Connecticut, I've been heavily involved in student organizations such as Sigma Phi Epsilon Fraternity, where I currently serve as the Vice President of Learning Community. Through HuskyTHON, I am currently a Dancer Representative, working to build morale and increase involvement within student organizations. As a chairman for the Balanced Man Scholarship, I managed operations and conducted interviews for the 2025 scholarship cycle. Through the UConn First Year Experience Programs, I mentored a class of first-year students, fostering academic and personal growth. All of these positions have helped me develop skills that are transferable to my career interests!
    </div>
  </div>
</section>

<section id=\"contact\">
  <div class=\"wrap\">
    <div class=\"section-head\">
      <h2>Contact</h2>
    </div>
    <p style=\"color:var(--text-soft); max-width:480px; margin-bottom:28px;\">
    <div class=\"contact-cards\">
      <a href=\"mailto:jakestark1@outlook.com\" class=\"contact-card\">
        <span class=\"contact-label\">Email</span>
        <span class=\"contact-value\">jakestark1@outlook.com</span>
      </a>
      <a href=\"https://www.linkedin.com/in/jake-stark-\" class=\"contact-card\">
        <span class=\"contact-label\">LinkedIn</span>
        <span class=\"contact-value\">linkedin.com/in/jake-stark-</span>
      </a>
      <a href=\"tel:+12014190069\" class=\"contact-card\">
        <span class=\"contact-label\">Phone</span>
        <span class=\"contact-value\">(201) 419-0069</span>
      </a>
    </div>
  </div>
</section>

</body>
</html>"""

# User customizable image formatting
image_max_width = "350px" # @param {type:"string"}
image_height = "auto" # @param {type:"string"}
image_alignment = "left" # @param ["left", "center", "right"] {type:"string"}
image_margin_top = "45px" # @param {type:"string"}

# Path to the uploaded image file
image_path = '/content/Arc Essex Logo.png'

# Read the image file in binary mode and encode it to Base64
with open(image_path, 'rb') as f:
    image_bytes = f.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

# Construct the data URI
data_uri = f'data:image/png;base64,{base64_image}'

# Path to the professional headshot image file
headshot_image_path = '/content/Professional Headshot.jpg'

# Read the headshot image file in binary mode and encode it to Base64
with open(headshot_image_path, 'rb') as f:
    headshot_image_bytes = f.read()
    headshot_base64_image = base64.b64encode(headshot_image_bytes).decode('utf-8')

# Construct the data URI for the headshot
headshot_data_uri = f'data:image/jpeg;base64,{headshot_base64_image}'

# Parse the original HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# --- Modify CSS to remove border-left and background from .field-notes ---
style_tag = soup.find('style')
if style_tag and style_tag.string:
    css_content = style_tag.string

    # Function to remove a specific CSS property from a block
    def remove_css_property(css_text, selector, prop_name):
        block_pattern = r'(' + re.escape(selector) + r'\s*\{[^}]*?)(' + re.escape(prop_name) + r':[^;]+;)(\s*[^}]*\})'
        return re.sub(block_pattern, r'\1\3', css_text, flags=re.DOTALL)

    css_content = remove_css_property(css_content, '.field-notes', 'border-left')
    css_content = remove_css_property(css_content, '.field-notes', 'background')

    style_tag.string = css_content # Update the style tag's content after all removals

# Find the <img> tag with alt='The Arc of Essex County Logo'
img_tag = soup.find('img', alt='The Arc of Essex County Logo')

if img_tag:
    # Update the src attribute of the found <img> tag
    img_tag['src'] = data_uri

    # Find the parent div with class 'field-notes' to adjust text-align
    parent_div = img_tag.find_parent('div', class_='field-notes')
    if parent_div:
        # Get current inline style, or an empty string if none exists
        current_inline_style = parent_div.get('style', '')

        # Remove any existing text-align property from the inline style
        updated_inline_style = re.sub(r'text-align\s*:\s*(left|center|right)\s*;?', '', current_inline_style)

        # Add the new text-align property based on image_alignment
        if image_alignment != "none":
            updated_inline_style += f'text-align: {image_alignment};'

        # Update the style attribute of the parent div
        parent_div['style'] = updated_inline_style.strip()

    # Update style attributes of the img tag based on user input, including margin-top
    img_tag['style'] = f"max-width: {image_max_width}; height: {image_height}; margin-top: {image_margin_top};"

# Find the <img> tag for the professional headshot
headshot_img_tag = soup.find('img', alt='Jake Stark')

if headshot_img_tag:
    # Update the src attribute of the headshot <img> tag
    headshot_img_tag['src'] = headshot_data_uri
    # Apply similar styling to the headshot image if desired (e.g., fixed size, aspect ratio)
    # The existing CSS rules for .about-me-photo img already handle basic styling.
    # You can add specific inline styles here if you want to override them from Python.
    headshot_img_tag['style'] = f"max-width: 100%; height: auto; object-fit: cover; aspect-ratio: 1/1; object-position: center 20%; transform: scale(0.9);"


# Get the modified HTML string
modified_html_content = str(soup)
# Display the updated HTML
display(HTML(modified_html_content))
