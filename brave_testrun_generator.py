from github import Github
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--test", help="Test Mode, do not create Github issues")

args = parser.parse_args()

secret_file = open('github.secret', 'r')
token_string = secret_file.readline().rstrip("\n\r")

wiki_laptop_file = open('wikitemplate.md', 'r')
laptop_template = wiki_laptop_file.read()

checklist = []
release_notes = []
exclusion_list = []
mac_checklist = []
win32_checklist = []
win64_checklist = []
linux_checklist = []

g = Github(token_string, timeout=1000)
rate = g.get_rate_limit()
limit = rate.rate.limit
remaining = rate.rate.remaining

repo_laptop = g.get_organization("brave").get_repo("browser-laptop")
repo_ios = g.get_organization("brave").get_repo("browser-ios")
repo_andriod = g.get_organization("brave").get_repo("browser-android-tabs")

laptop_milestone = {}
for milestone in repo_laptop.get_milestones(state="open"):
  laptop_milestone.update({milestone.title:milestone})

ios_milestone = {}
for milestone in repo_ios.get_milestones(state="open"):
  ios_milestone.update({milestone.title:milestone})

andriod_milestone = {}
for milestone in repo_andriod.get_milestones(state="open"):
  andriod_milestone.update({milestone.title:milestone})

def laptop_release_channel():

  laptop_key = sorted(laptop_milestone.keys())[0]
   
  print(laptop_key)

  for issue in repo_laptop.get_issues(milestone=laptop_milestone[laptop_key], state="closed"):
    if('pull' not in issue.html_url):
      original_issue_title = issue.title
      issue_title = original_issue_title
      if(original_issue_title[0].islower()):
        lower = original_issue_title[0]
        upper = original_issue_title[0].upper()
        issue_title = original_issue_title.replace(lower, upper, 1)

    labels = issue.get_labels()
    label_names = []
    for label in labels:
      label_names.append(label.name)
    if('release-notes/include' in label_names or 'release-notes/exclude' in label_names and 'tests' not in label_names):
      output_line = ' - [ ] ' + issue_title + '. ([#' + str(issue.number) + '](' + issue.html_url + '))'
      checklist.append(output_line)

    if('QA/test-plan-specified' in label_names or 'QA/test-plan-required' in label_names and 'QA/no-qa-needed' not in label_names):
      output_line = ' - [ ] ' + issue_title + '.([#' + str(issue.number) + '](' + issue.html_url + '))'
      checklist.append(output_line)
      checklist.append(issue.html_url)
      if('QA/checked-macOS' not in label_names and 'QA/checked' not in label_names and 'OS/Windows' not in label_names and 'OS/unix-like/linux' not in label_names):
        mac_checklist.append(output_line)

      if('QA/checked-Win64' not in label_names and 'QA/checked' not in label_names and 'OS/macOS' not in label_names and 'OS/unix-like/linux' not in label_names):
        win64_checklist.append(output_line)
      
      if('QA/checked-Linux' not in label_names and 'QA/checked' not in label_names and 'OS/Windows' not in label_names and 'OS/macOS' not in label_names):
        linux_checklist.append(output_line)

      else:
        output_line = ' - [ ] ' + issue_title + '. ([#' + str(issue.number) + '](' + issue.html_url + '))'
        exclusion_list.append(output_line)
        exclusion_list.append(issue.html_url)

  print("Release Notes: ")
  for line in release_notes:
    print(line)
  print("")

  print("Checklist: ")
  for line in checklist:
    print(line)
  print("")

  print("Exclusion List: ")
  for line in exclusion_list:
    print(line)
  print("")

  print("Mac Checklist: ")
  bigline = "## Per release speciality tests\n"
  for line in mac_checklist:
    bigline += line + "\n"
  bigline = bigline + laptop_template
  print(bigline)
  print("")
  macTitle = "Manual test run on OS X for " + laptop_key
  macList = ['OS/macOS', 'release-notes/exclude', 'tests']

  if args.test is None:
    laptop_repo.create_issue(title="macTitle",body=bigline,assignee="LaurenWags",milestone=laptop_milestone[laptop_key],labels=macList)

  print("Win64 Checklist: ")
  bigline = "## Per release speciality tests\n"
  for line in win64_checklist:
    bigline += line + "\n"
  bigline = bigline + laptop_template
  print(bigline)
  print("")
  winTitle = "Manual test run on Windows 64 for " + laptop_key
  winList = ['OS/Windows', 'release-notes/exclude', 'tests']

  if args.test is None:
    laptop_repo.create_issue(title="winTitle",body=bigline,assignee="srirambv",milestone=laptop_milestone[laptop_key],labels=winList)

  print("Linux Checklist: ")
  bigline = "## Per release speciality tests\n"
  for line in linux_checklist:
    bigline += line + "\n"
  bigline = bigline + laptop_template
  print(bigline)
  print("")
  linuxTitle = "Manual test run on Linux for " + laptop_key
  linuxList = ['OS/unix-like/linux', 'release-notes/exclude', 'tests']

  if args.test is None:
    laptop_repo.create_issue(title="linuxTitle",body=bigline,assignee="kjozwiak",milestone=laptop_milestone[laptop_key],labels=linuxList)


  return

def laptop_beta_channel():

  return

def laptop_developer_channel():

  return

def chromium_release_channel():

  laptop_key = sorted(laptop_milestone.keys())[0]
   
  print(laptop_key)

  for issue in repo_laptop.get_issues(milestone=laptop_milestone[laptop_key], state="closed"):
    if('pull' not in issue.html_url):
      original_issue_title = issue.title
      issue_title = original_issue_title
      if(original_issue_title[0].islower()):
        lower = original_issue_title[0]
        upper = original_issue_title[0].upper()
        issue_title = original_issue_title.replace(lower, upper, 1)

    labels = issue.get_labels()
    label_names = []
    for label in labels:
      label_names.append(label.name)
    if('release-notes/include' in label_names or 'release-notes/exclude' in label_names and 'tests' not in label_names):
      output_line = ' - [ ] ' + issue_title + '. ([#' + str(issue.number) + '](' + issue.html_url + '))'
      checklist.append(output_line)
      checklist.append(issue.html_url)
      if('QA/checked-macOS' not in label_names and 'QA/checked' not in label_names and 'OS/Windows' not in label_names and 'OS/unix-like/linux' not in label_names):
        mac_checklist.append(output_line)

      if('QA/checked-Win64' not in label_names and 'QA/checked' not in label_names and 'OS/macOS' not in label_names and 'OS/unix-like/linux' not in label_names):
        win64_checklist.append(output_line)
      
      if('QA/checked-Linux' not in label_names and 'QA/checked' not in label_names and 'OS/Windows' not in label_names and 'OS/macOS' not in label_names):
        linux_checklist.append(output_line)

      else:
        output_line = ' - [ ] ' + issue_title + '. ([#' + str(issue.number) + '](' + issue.html_url + '))'
        exclusion_list.append(output_line)
        exclusion_list.append(issue.html_url)

  print("Release Notes: ")
  for line in release_notes:
    print(line)
  print("")

  print("Checklist: ")
  for line in checklist:
    print(line)
  print("")

  print("Exclusion List: ")
  for line in exclusion_list:
    print(line)
  print("")

  print("Mac Checklist: ")
  bigline = "## Per release speciality tests\n"
  for line in mac_checklist:
    bigline += line + "\n"
  bigline = bigline + laptop_template
  print(bigline)
  print("")
  macTitle = "Manual test run on OS X for " + laptop_key
  macList = ['OS/macOS', 'release-notes/exclude', 'tests']

  if args.test is None:
    laptop_repo.create_issue(title="macTitle",body=bigline,assignee="LaurenWags",milestone=laptop_milestone[laptop_key],labels=macList)

  print("Win64 Checklist: ")
  bigline = "## Per release speciality tests\n"
  for line in win64_checklist:
    bigline += line + "\n"
  bigline = bigline + laptop_template
  print(bigline)
  print("")
  winTitle = "Manual test run on Windows 64 for " + laptop_key
  winList = ['OS/Windows', 'release-notes/exclude', 'tests']

  if args.test is None:
    laptop_repo.create_issue(title="winTitle",body=bigline,assignee="srirambv",milestone=laptop_milestone[laptop_key],labels=winList)

  print("Linux Checklist: ")
  bigline = "## Per release speciality tests\n"
  for line in linux_checklist:
    bigline += line + "\n"
  bigline = bigline + laptop_template
  print(bigline)
  print("")
  linuxTitle = "Manual test run on Linux for " + laptop_key
  linuxList = ['OS/unix-like/linux', 'release-notes/exclude', 'tests']

  if args.test is None:
    laptop_repo.create_issue(title="linuxTitle",body=bigline,assignee="kjozwiak",milestone=laptop_milestone[laptop_key],labels=linuxList)

  return

def chroium_beta_channel():
  return
  
def chromium_developer_channel():
  return

def prerel_release_channel():
  laptop_key = sorted(laptop_milestone.keys())[0]
   
  print(laptop_key)

  for issue in repo_laptop.get_issues(milestone=laptop_milestone[laptop_key], state="closed"):
    if('pull' not in issue.html_url):
      original_issue_title = issue.title
      issue_title = original_issue_title
      if(original_issue_title[0].islower()):
        lower = original_issue_title[0]
        upper = original_issue_title[0].upper()
        issue_title = original_issue_title.replace(lower, upper, 1)

    labels = issue.get_labels()
    label_names = []
    for label in labels:
      label_names.append(label.name)
    if('release-notes/include' in label_names or 'release-notes/exclude' in label_names and 'tests' not in label_names):
      output_line = ' - [ ] ' + issue_title + '. ([#' + str(issue.number) + '](' + issue.html_url + '))'
      checklist.append(output_line)
      checklist.append(issue.html_url)
      if('QA/checked-macOS' not in label_names and 'QA/checked' not in label_names and 'OS/Windows' not in label_names and 'OS/unix-like/linux' not in label_names):
        mac_checklist.append(output_line)

      if('QA/checked-Win64' not in label_names and 'QA/checked' not in label_names and 'OS/macOS' not in label_names and 'OS/unix-like/linux' not in label_names):
        win64_checklist.append(output_line)
      
      if('QA/checked-Linux' not in label_names and 'QA/checked' not in label_names and 'OS/Windows' not in label_names and 'OS/macOS' not in label_names):
        linux_checklist.append(output_line)

      else:
        output_line = ' - [ ] ' + issue_title + '. ([#' + str(issue.number) + '](' + issue.html_url + '))'
        exclusion_list.append(output_line)
        exclusion_list.append(issue.html_url)

  print("Release Notes: ")
  for line in release_notes:
    print(line)
  print("")

  print("Checklist: ")
  for line in checklist:
    print(line)
  print("")

  print("Exclusion List: ")
  for line in exclusion_list:
    print(line)
  print("")

  print("Mac Checklist: ")
  bigline = "## Per release speciality tests\n"
  for line in mac_checklist:
    bigline += line + "\n"
  print(bigline)
  print("")
  macTitle = "Manual test run on OS X for " + laptop_key
  macList = ['OS/macOS', 'release-notes/exclude', 'tests']

  if args.test is None:
    laptop_repo.create_issue(title="macTitle",body=bigline,assignee="LaurenWags",milestone=laptop_milestone[laptop_key],labels=macList)

  print("Win64 Checklist: ")
  bigline = "## Per release speciality tests\n"
  for line in win64_checklist:
    bigline += line + "\n"
  print(bigline)
  print("")
  winTitle = "Manual test run on Windows 64 for " + laptop_key
  winList = ['OS/Windows', 'release-notes/exclude', 'tests']

  if args.test is None:
    laptop_repo.create_issue(title="winTitle",body=bigline,assignee="srirambv",milestone=laptop_milestone[laptop_key],labels=winList)

  print("Linux Checklist: ")
  bigline = "## Per release speciality tests\n"
  for line in linux_checklist:
    bigline += line + "\n"
  print(bigline)
  print("")
  linuxTitle = "Manual test run on Linux for " + laptop_key
  linuxList = ['OS/unix-like/linux', 'release-notes/exclude', 'tests']

  if args.test is None:
    laptop_repo.create_issue(title="linuxTitle",body=bigline,assignee="kjozwiak",milestone=laptop_milestone[laptop_key],labels=linuxList)

  return

def prerel_beta_channel():
  return

def prerel_developer_channel():
  return

def iostest():
  iOS10_iPad_checklist = []
  iOS11_iPad_checklist = []
  iOS10_iPhone6_checklist = []
  iOS11_iPhone7_checklist = []

  wikitemplate_ios = open('wikitemplate-ios.md', 'r')
  ios_template = wikitemplate_ios.read()

  ios_repo = g.get_organization("brave").get_repo("browser-ios")

  ios_key = sorted(ios_milestone.keys())[0]

  iOS10_iPad_checklist = []
  iOS11_iPad_checklist = []
  iOS10_iPhone6_checklist = []
  iOS11_iPhone7_checklist = []

  for issue in repo_ios.get_issues(milestone=ios_milestone[ios_key], state="closed"):
    if('pull' not in issue.html_url):
      original_issue_title = issue.title
      issue_title = original_issue_title
      if(original_issue_title[0].islower()):
        lower = original_issue_title[0]
        upper = original_issue_title[0].upper()
        issue_title = original_issue_title.replace(lower, upper, 1)

      labels = issue.get_labels()
      label_names = []
      for label in labels:
        label_names.append(label.name)
      if('release-notes/include' in label_names or 'release-notes/exclude' in label_names and 'tests' not in label_names):
        output_line = ' - [ ] ' + issue_title + '. ([#' + str(issue.number) + '](' + issue.html_url + '))'
        release_notes.append(output_line)

      if('QQA/Steps-specified' in label_names or 'QA/Steps-Required' in label_names and 'QA/no-qa-needed' not in label_names):
        output_line = ' - ' + issue_title + '. ([#' + str(issue.number) + '](' + issue.html_url + '))'
        checklist.append(output_line)
        checklist.append(issue.html_url)
        if('checked by qa - iOS10 iPad' not in label_names and 'checked by qa' not in label_names):
          iOS10_iPad_checklist.append(output_line)

        if('checked by qa - iOS11 iPad' not in label_names and 'checked by qa' not in label_names):
          iOS11_iPad_checklist.append(output_line)  

        if('checked by qa - iPhone 6 (iOS10)' not in label_names and 'checked by qa' not in label_names):
          iOS10_iPhone6_checklist.append(output_line)

        if('checked by qa - iPhone 7+ (iOS11)' not in label_names and 'checked by qa' not in label_names):
          iOS11_iPhone7_checklist.append(output_line)

      else:
        output_line = ' - [ ] ' + issue_title + '([#' + str(issue.number) + '](' + issue.html_url + '))'
        exclusion_list.append(output_line)
        exclusion_list.append(issue.html_url)
  print("Release Note:")
  for line in release_notes:
    print(line)
  print("")

  print("Release Checklist:")
  for line in checklist:
    print(line)
  print("")

  print("Exclusion List:")
  for line in exclusion_list:
    print(line)
  print("")

  print("iOS10 iPad Checklist:")
  bigline = "## Per release speciality tests\n"
  for line in iOS10_iPad_checklist:
    bigline += line + "\n"
  bigline = bigline + ios_template
  print(bigline)
  print("")
  iOS10iPadTitle = "Manual test run for iOS10 iPad for " + ios_key
  iOS10iPadList = ['ipadp', 'release-notes/exclude', 'tests']

  if args.test is None:
    ios_repo.create_issue(title=iOS10iPadTitle,body=bigline,asignee="LaurenWags",milestone=milestone_dictionary[ios_key],labels=iOS10iPadList)

  print("iOS11 iPad Checklist:")
  bigline = "## Per release speciality tests\n"
  for line in iOS11_iPad_checklist:
    bigline += line + "\n"
  bigline = bigline + ios_template
  print(bigline)
  print("")
  iOS11iPadTitle = "Manual test run for iOS11 iPad for " + ios_key
  iOS11iPadList = ['ipadp', 'release-notes/exclude', 'tests']

  if args.test is None:
    ios_repo.create_issue(title=iOS11iPadTitle,body=bigline,asignee="srirambv",milestone=milestone_dictionary[ios_key],labels=iOS11iPadList)

  print("iOS10 iPhone6 Checklist:")
  bigline = "## Per release speciality tests\n"
  for line in iOS10_iPhone6_checklist:
    bigline += line + "\n"
  bigline = bigline + ios_template
  print(bigline)
  print("")
  iOS10iPhone6Title = "Manual test run for iOS10 iPhone 6 for " + ios_key
  iOS10iPhone6List = ['ipadp', 'release-notes/exclude', 'tests']

  if args.test is None:
    ios_repo.create_issue(title=iOS10iPhone6Title,body=bigline,asignee="LaurenWags",milestone=milestone_dictionary[ios_key],labels=iOS10iPhone6List)

  print("iOS11 iPhone7 Checklist:")
  bigline = "## Per release speciality tests\n"
  for line in iOS11_iPhone7_checklist:
    bigline += line + "\n"
  bigline = bigline + ios_template
  print(bigline)
  print("")
  iOS11iPhone7Title = "Manual test run for iOS11 iPhone7+ for " + ios_key
  iOS11iPhone7List = ['ipadp', 'release-notes/exclude', 'tests']

  if args.test is None:
    ios_repo.create_issue(title=iOS11iPhone7Title,body=bigline,asignee="srirambv",milestone=milestone_dictionary[ios_key],labels=iOS11iPhone7List)

  return

def androidtest():
  wikitemplate_android = open('wikitemplate-android.md','r')
  andriod_template = wikitemplate_android.read()

  andriod_repo = g.get_organization("brave").get_repo("browser-android-tabs")

  andriod_key = sorted(andriod_milestone.keys())[0]
  
  android_x86_checklist = []
  android_arm_checklist = []

  for issue in andriod_repo.get_issues(milestone=andriod_milestone[andriod_key], state="closed"):
    if('pull' not in issue.html_url):
      original_issue_title = issue.title
      issue_title = original_issue_title
      if(original_issue_title[0].islower()):
        lower = original_issue_title[0]
        upper = original_issue_title[0].upper()
        issue_title = original_issue_title.replace(lower, upper, 1)
        #print(issue_title)

      labels = issue.get_labels()
      #print(labels)
      label_names = []
      for label in labels:
        label_names.append(label.name)
      if('release-notes/include' in label_names or 'release-notes/exclude' in label_names and 'tests' not in label_names):
        output_line = ' - ' + issue_title + '.([#' + str(issue.number) + '])' + issue.html_url + '))'
        release_notes.append(output_line)

      if('QA/steps-specified' in label_names and 'QA/no-qa-needed' not in label_names):
        output_line = ' - [ ] ' + issue_title + '. ([#' + str(issue.number) + '])' + issue.html_url + '))'
        checklist.append(output_line)
        checklist.append(issue.html_url)
        if('checked by qa - Android ARM' not in label_names and 'checked by qa' not in label_names):
          android_arm_checklist.append(output_line)

        if('checked by qa - Andriod x86' not in label_names and 'checked by qa' not in label_names):
          android_x86_checklist.append(output_line)

      else:
        output_line = ' - [ ] ' + issue_title + '. ([#' + str(issue.number) + '](' + issue.html_url + '))'
        exclusion_list.append(output_line)
        exclusion_list.append(issue.html_url)

  print("Release Notes:")
  for line in release_notes:
    print(line)
  print("")

  print("Checklist:")
  for line in checklist:
    print(line)
  print("")

  print("Exclusion List:")
  for line in exclusion_list:
    print(line)
  print("")

  print("Android ARM Checklist:")
  bigline = "## Per release speciality tests\n"
  for line in android_arm_checklist:
    bigline += line + "\n"
  bigline = bigline + andriod_template
  print(bigline)
  print("")
  AndriodARMtitle = "Manual test run on Andriod ARM " + andriod_key
  AndriodARMlist = ['ARM', 'release-notes/exclude', 'tests']

  if args.test is None:
    andriod_repo.create_issue(title=AndriodARMtitle,body=bigline,assignee="LaruenWags",milestone=andriod_milestone[andriod_key],labels=AndriodARMlist)

  print("Android x86 Checklist:")
  bigline = "## Per release specilaity tests\n"
  for line in android_arm_checklist:
    bigline += line + "\n"
  bigline = bigline + andriod_template
  print(bigline)
  print("")
  AndriodARMtitle = "Manual test run on Andriod x86 " + andriod_key
  AndriodARMlist = ['x86', 'release-notes/exclude', 'tests']

  if args.test is None:
    andriod_repo.create_issue(title=AndriodARMtitle,body=bigline,assignee="srirambv",milestone=andriod_milestone[andriod_key],labels=AndriodARMlist)

  return

print('**************************************************************************************************************************')
print('                         Few things to check before generating test runs')
print('')
print('1. Ensure all closed items have release-notes/include , release-notes/exclude and QA/test-plan-specified label added')
print('')
print('2. For iOS, rename QA/NO-QA required to QA/no-qa-needed in Github before running')
print('**************************************************************************************************************************')

header = print("Create test runs for:\n")
laptop = print("1. Laptop Release")
laptopcr = print("2. Laptop Chromium Release")
laptop_per = print("3. Laptop Per-release Checklist")
ios = print("4. iOS")
android = print("5. Andriod\n")

select_checklist = input("Choose the platform for which you want to generate the test run: ")

if(select_checklist == '1' or select_checklist == '2' or select_checklist == '3'):
  print("\nSelect the channel to create tests \n")
  print("1. Release Channel")
  print("2. Beta Channel")
  print("3. Developer Channel\n")
  
  generate_test = input("Create test runs for: ")
  
  if(select_checklist == "1" and generate_test == "1"):
    print("Generating test runs for Laptop Release Channel on all platforms")
    laptop_release_channel()
  elif(select_checklist == "1" and generate_test == "2"):
    print("Generating test runs for Laptop Beta Channel on all platforms")
    laptop_beta_channel()
  elif(select_checklist == "1" and generate_test == "3"):
    print("Generating test runs for Laptop Developer Channel on all platforms")
    laptop_developer_channel()
  elif(select_checklist == "2" and generate_test == "1"):
    print("Generating test runs for Release Channel Chromium upgrade on all platforms")
    chromium_release_channel()
  elif(select_checklist == "2" and generate_test == "2"):
    print("Generating test runs for Beta Channel Chromium upgrade on all platforms")
    chroium_beta_channel()
  elif(select_checklist == "2" and generate_test == "3"):
    print("Generating test runs for Developer Channel  Chromium upgrade on all platforms")
    chromium_developer_channel()
  elif(select_checklist == "3" and generate_test == "1"):
    print("Generating test runs for Release Channel Per-release checklist on all platforms")
    prerel_release_channel()
  elif(select_checklist == "3" and generate_test == "2"):
    print("Generating test runs for Beta Channel Per-release checklist on all platforms")
    prerel_beta_channel()
  elif(select_checklist == "3" and generate_test == "3"):
    print("Generating test runs for Developer Channel Per-release checklist on all platforms")
    prerel_developer_channel()
  else:
    print("Invalid selection. Exiting test creation...")
    exit()

elif (select_checklist == '4'):
  generate_ios_test = print("Generating test runs for iOS ",sorted(ios_milestone.keys())[0])
  iostest()
elif (select_checklist == '5'):
  generate_andriod_test = print("Generating test runs for Andriod",sorted(andriod_milestone.keys())[0])
  androidtest()
else: 
  print("Incorrect selection. Exiting test creation...")
  exit()