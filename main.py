import os

import wx
from openai import OpenAI

client = OpenAI()


class SnarkyApp(wx.Frame):
    """
    Class representing a 'Snarky App' utilizing wxPython frames.
    """

    BORDER = 5

    def __init__(self, *args, **kw):
        """
        Initialize the frame and UI elements.
        """
        super(SnarkyApp, self).__init__(*args, **kw)
        self.snarkiness_slider = None
        self.snarkiness_value = 5
        self.snarkiness_label = f"Snarkiness Level {self.snarkiness_value}/10"
        self.answer_box = None
        self.comment_box = None
        self.api_key_txt = None
        self.api_key_status_txt = None
        self.api_key_status = ""
        self.init_ui()
        self.SetTitle('Snarky Answering Machine (S.A.M.)')
        self.Centre()
        self.check_api_key()

    def init_ui(self):
        """
        Create UI elements.
        """
        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        comment_label = wx.StaticText(pnl, label='Comment:')
        self.comment_box = wx.TextCtrl(pnl, style=wx.TE_MULTILINE | wx.TE_RICH2, size=(600, 200))
        answer_label = wx.StaticText(pnl, label='Answer:')
        self.answer_box = wx.TextCtrl(pnl, style=wx.TE_MULTILINE | wx.TE_RICH2 | wx.TE_READONLY, size=(-1, 300))
        self.snarkiness_slider = wx.Slider(pnl, value=5, minValue=0, maxValue=10, style=wx.SL_HORIZONTAL)
        self.snarkiness_slider.Bind(wx.EVT_SLIDER, self.on_snarkiness_change)
        self.snarkiness_label = wx.StaticText(pnl, label=self.snarkiness_label)

        submit_btn = wx.Button(pnl, label='Submit')
        submit_btn.Bind(wx.EVT_BUTTON, self.on_submit)

        self.api_key_txt = wx.TextCtrl(pnl)
        self.api_key_txt.Bind(wx.EVT_KILL_FOCUS, self.on_api_key_change)
        self.api_key_status_txt = wx.StaticText(pnl, label=self.api_key_status)

        components = [self.api_key_status_txt, self.api_key_txt, comment_label, self.comment_box, self.snarkiness_label, self.snarkiness_slider,
                      submit_btn, answer_label, self.answer_box]
        for component in components:
            vbox.Add(component, proportion=0, flag=wx.EXPAND | wx.ALL, border=self.BORDER)

        pnl.SetSizer(vbox)
        vbox.Fit(self)

    def on_submit(self, event):
        """
        Called when submit button is clicked.
        """
        # Here you would call the OpenAI API with the comment and snarkiness level
        # This example just echoes the comment and snarkiness level back
        comment = self.comment_box.GetValue()
        snarkiness = self.snarkiness_slider.GetValue()
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system",
                 "content": "Create a snarky response to a toxic or nasty comment turning sexist or bigoted comments around to verbally wrestle the commenter down. Avoid starting answers with \"Ah, yes\" or \"Oh, bless your heart\". Use something more unpredictable and clever to hide your sarcasm and satire. Never defend the subject of the toxic commentary. Always turn the attack of the commenter. Keep responses short. Always answer in the same language as the user."},
                {"role": "user",
                 "content": "Comment: \"Matti Meikäläinen\nHeidi, onko sulla käynyt mielessä, että hän voisi olla oikeassa? Oletko miettinyt sellaista mahdollisuutta, että koska et pysty nähtävästi millään tasolla argumentoimaan hänen kantojaan vastaan faktoilla, tilastoilla tai tutkimuksilla, vaan ainoa työkalu jolla voit heidän näkemyksiään vastustaa on mustamaalaaminen, niin vika ei välttämättä ole hänessä tai heissä, vaan saatat yksinkertaisesti olla väärässä? Edit: Taas on osalta kommentoijista unohtunut, että nauruhymiö on kannanotto kommentin puolesta, ei sitä vastaan, jos ei muuten pysty esittämään vedenpitävää vasta-argumenttia. 🤷🏼‍\", Snarkiness Level: 5/10"},
                {"role": "assistant",
                 "content": "Vau, Matti, sinähän olet asettanut itsesi internetin ylivoimaiseksi totuuden tuomariksi. On virkistävää nähdä jonkun astuvan niin itsevarmasti keskusteluihin vankkumattomalla uskolla siihen, että juuri hänellä, ja vain hänellä, on jumalallinen kyky erottaa totuus taruista ilman mitään tarvetta hankalille asioille kuten empatialle tai ymmärrykselle. Ja tuo mullistava oivalluksesi, että erimielisyys ilman tilastollista näyttöä on mustamaalaamista? Todella, teet Herran työtä kommenttiosiossa. Ihme, että olemme selvinneet ilman viisauttasi näin kauan.\n\n"},
                {"role": "user",
                 "content": f"Comment: \"{comment}\", Snarkiness Level: {snarkiness}/10"},
            ]
        )
        answer = completion.choices[0].message.content

        # Append the response to the answerBox
        self.answer_box.AppendText(f"Snarkiness: {snarkiness}\n{answer}\n\n")

    def check_api_key(self):
        """
        Check if openai_api_key exists and works
        """
        client.api_key = self.api_key_txt.GetValue() or os.getenv("OPENAI_API_KEY")

        try:
            status = bool(client.models.list())
        except Exception:
            print("Invalid API key")
            status = False

        self.api_key_status = status
        self.api_key_status_txt.SetLabel(f"API key valid: {self.api_key_status}")
        return status

    def on_api_key_change(self, event):
        """
        Called when the API key text box is changed.
        """
        # Set the environment variable to the new value
        self.check_api_key()

    def on_snarkiness_change(self, event):
        """
        Called when the snarkiness slider is changed.
        """
        self.snarkiness_value = self.snarkiness_slider.GetValue()
        self.snarkiness_label.SetLabel(f"Snarkiness Level {self.snarkiness_value}/10")


def main():
    app = wx.App(False)
    frame = SnarkyApp(None)
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    main()
