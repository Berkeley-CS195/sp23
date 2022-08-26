import os
import re
import templar
from templar.api.rules.core import SubstitutionRule
from templar.api.rules.compiler_rules import MarkdownToHtmlRule
from templar.api.rules.table_of_contents import HtmlTableOfContents
from templar.api.config import ConfigBuilder

# Import various utilities from utils
# import templar.utils.html
# import templar.utils.filters

# Path of the current file -- best not to change this
FILEPATH = os.path.dirname(os.path.abspath(__file__))

##################
# Configurations #
##################


# v2 config file
#class UpperCaseRule(SubstitutionRule):
#    pattern = r'(\w*)'
#    def substitute(self, match):
#        return match.group(1).upper()

config = ConfigBuilder().add_template_dirs(
    # The 'templates' folder is specified explicitly.
    FILEPATH,
    # Templates no longer need to be placed in a directory called 'templates'
    os.path.join(FILEPATH, 'templates')
).add_variables({
}).append_compiler_rules(
    MarkdownToHtmlRule(),
).append_postprocess_rules(
    #UpperCaseRule(src='md$', dst='html$'),
    HtmlTableOfContents(),
).build()
