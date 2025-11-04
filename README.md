# Galaxy Extensions (Ansible role)

A collection of Galaxy extensions (AKA webhooks) in an Ansible role for rapid
deployment to Galaxy servers


Extension       | Author    | Responsibility
--------------- | --------- | --------------
citation_needed | Galaxy EU | Shows how to cite us randomly after jobs
gtn             | Galaxy EU | Embed GTN in Galaxy
iframe          | Galaxy EU | Shows a random iframe after jobs
phdcomics       | Galaxy EU | Shows a random phd comic after jobs
search          | Galaxy EU | Shows the search interface
tool_list       | Galaxy EU | Adds a button to generate the tool list
tour_generator  | Galaxy EU | Adds support for tour generator
lab_switcher    | Galaxy AU | Easily navigate between Galaxy Labs
toolmsg         | Galaxy AU | User-facing messages on specific tools
tips            | Galaxy AU | Show random Galaxy tip after jobs


## Directory structure

Each extension is versioned by Galaxy version, to accomodate breaking changes in
Galaxy releases. The Ansible role should install the highest version available
that is less than or equal to the Galaxy version on the host.


## Templating

Any extension can be templated by adding a .j2 extension to the file name. Any
variables available in the running playbook can be used, but defaults should be
set in defaults/extensions.yml to ensure predictable results, and document the
variables being used for users of the Ansible role.
