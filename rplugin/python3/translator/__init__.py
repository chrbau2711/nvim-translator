import neovim
from translator.translator import Translator


@neovim.plugin
class TranslatorHandler(object):
    """The remote translator plugin for neovim.
    """
    def __init__(self, vim):
        """Initializes the translator plugin.

        :vim: Holds the vim instance.
        :returns: The translator instance.

        """
        self._vim = vim

    @neovim.command('TranslateLine', range='', nargs='*', sync=True)
    def translate_line(self, args, nvim_range):
        """Translates line-wise.

        :args: A list containing 2 elements: [<source>, <target>]
        :nvim_range: The range of Lines to translate.
        :returns: Nothing. But replaces the current or selected lines.

        """
        if len(args) is 2:
            source = args[0]
            target = args[1]
        elif len(args) is 1:
            source = "auto"
            # TODO: Let user specify defaults.
            target = "EN"
        elif len(args) is 0:
            # TODO: Let user specify defaults.
            source = "DE"
            target = "EN"
        else:
            self.print_error_in_vim("TranslateLine takes either 0 or 2 arguments")
            self.print_error_in_vim("TranslateLine [[<source>] <target>]")
            return
        lines = self._vim.current.buffer[nvim_range[0]-1 : nvim_range[1]]
        translated_lines = [self.translate(source, target, line) for line in lines]
        self._vim.current.buffer[nvim_range[0]-1 : nvim_range[1]] = translated_lines

    def print_error_in_vim(self, msg):
        self._vim.command("echohl Error | echomsg '[translator]: " + msg + "' | echohl None")

    def translate(self, source, target, string):
        """Translates the string from source to target language.

        :source: Source language identifier.
        :target: Target language identifier.
        :string: The string to translate.
        :returns: The translated string or -1.

        """
        from subprocess import run
        from subprocess import PIPE

        completed_process = run(["deepl", "-s", source, "-t", target, "translate", string], stdout=PIPE, encoding="utf-8")
        return completed_process.stdout.strip()
