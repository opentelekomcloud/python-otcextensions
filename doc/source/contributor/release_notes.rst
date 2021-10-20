Add Release Notes with Reno
===========================

Reno is a Python application which is used to add release notes to your Pull
Request.

(Optional) Activate your Python virtual environment which is an optional step.

.. code-block:: bash

   source <python-virtal-env>/bin/activate

Install Reno with the following command.

.. code-block:: bash

   pip install reno

Switch to root folder of the cloned repository of OTCExtensions and add a new
release notes file template with Reno. Switch into the file to add your
specific informations in the proper section.

.. code-block:: bash

   reno new <file-name>

The sections not being used can be deleted.

.. code-block:: bash

   nano releasenotes/notes/<file-name>
   ---
   prelude: >
      Replace this text with content to appear at the top of the section for this
      release. All of the prelude content is merged together and then rendered
      separately from the items listed in other parts of the file, so the text
      needs to be worded so that both the prelude and the other items make sense
      when read independently. This may mean repeating some details. Not every
      release note requires a prelude. Usually only notes describing major
      features or adding release theme details should have a prelude.
   features:
   - |
      List new features here, or remove this section.  All of the list items in
      this section are combined when the release notes are rendered, so the text
      needs to be worded so that it does not depend on any information only
      available in another section, such as the prelude. This may mean repeating
      some details.
   issues:
   - |
      List known issues here, or remove this section.  All of the list items in
      this section are combined when the release notes are rendered, so the text
      needs to be worded so that it does not depend on any information only
      available in another section, such as the prelude. This may mean repeating
      some details.
   upgrade:
   - |
      List upgrade notes here, or remove this section.  All of the list items in
      this section are combined when the release notes are rendered, so the text
      needs to be worded so that it does not depend on any information only
      available in another section, such as the prelude. This may mean repeating
      some details.
   deprecations:
   - |
      List deprecations notes here, or remove this section.  All of the list
      items in this section are combined when the release notes are rendered, so
      the text needs to be worded so that it does not depend on any information
      only available in another section, such as the prelude. This may mean
      repeating some details.
   critical:
   - |
      Add critical notes here, or remove this section.  All of the list items in
      this section are combined when the release notes are rendered, so the text
      needs to be worded so that it does not depend on any information only
      available in another section, such as the prelude. This may mean repeating
      some details.
   security:
   - |
      Add security notes here, or remove this section.  All of the list items in
      this section are combined when the release notes are rendered, so the text
      needs to be worded so that it does not depend on any information only
      available in another section, such as the prelude. This may mean repeating
      some details.
   fixes:
   - |
      Add normal bug fixes here, or remove this section.  All of the list items
      in this section are combined when the release notes are rendered, so the
      text needs to be worded so that it does not depend on any information only

Push your changes upstream.

.. code-block:: bash

   git add releasenotes/notes/<file-name>
   git commit
   git push
