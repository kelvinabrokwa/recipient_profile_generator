from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# register Open Sans
pdfmetrics.registerFont(TTFont('Open Sans', 'assets/fonts/fonts-open-sans/OpenSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Open Sans Bold', 'assets/fonts/fonts-open-sans/OpenSans-Bold.ttf'))

class RecipientProfile:

    def __init__(self, rec):
        self.rec = rec
        self.c = canvas.Canvas(rec + '.pdf')
        self.PAGEWIDTH, self.PAGEHEIGHT = letter
        self.chart = {}
        self.chart['pie_width'] = 170
        self.chart['pie_height'] = 170
        self.chart['pie_title_y_offset'] = 170
        self.chart['pie_title_x_offset'] = 40

        self.debug = True

        self.template().add_charts()

    def template(self):
        self.draw_header()
        return self

    def draw_header(self):
        height_blue = 70
        x_offset_blue = 0
        y_offset_blue = self.PAGEHEIGHT + 50 - height_blue

        # blue header
        self.c.setFillColorRGB(.086, .121, .203)
        self.c.rect(x_offset_blue, y_offset_blue, self.PAGEWIDTH, height_blue, fill=1)
        self.c.setFillColor(colors.white)
        self.c.setFont('Open Sans', 20)
        #self.c.drawString(headboxx, headboxy + .425 * headboxh, 'Partner Country Profile')

        # green header
        height_green = 30
        x_offset_green = 0
        y_offset_green = y_offset_blue - height_green
        self.c.setFillColorRGB(0.46, 0.71, 0.34)
        self.c.rect(x_offset_green, y_offset_green, self.PAGEWIDTH, height_green, fill=1)

        return self


    def add_charts(self):
        self.draw_pie_legend()
        self.draw_dac()
        self.draw_nondac()
        self.draw_multi()
        self.draw_bars()
        self.draw_agenda()
        self.draw_usefulness()
        self.draw_helpfulness()
        self.draw_avg_influence()
        self.draw_footer()
        return self

    def draw_pie_legend(self):
        x_offset = 40
        y_offset = 350

        if self.debug:
            self.c.rect(x_offset, y_offset, 100, 100)

    def draw_dac(self):
        # location
        x_offset = 50
        y_offset = 490
        title_x = x_offset + self.chart['pie_title_x_offset']
        title_y = y_offset + self.chart['pie_title_y_offset']
        chart_x = x_offset
        chart_y = y_offset

        if self.debug:
            self.c.rect(x_offset, y_offset, 200, 200)

        # draw title
        title = 'Top 5 DAC Development Partners'
        p = Paragraph(title, getSampleStyleSheet()['Normal'])
        p.wrapOn(self.c, 100, 100)
        p.drawOn(self.c, title_x, title_y)

        # draw chart
        chart = 'charts/pie_chart_' + self.rec + '_dac.png'
        self.c.drawImage(chart, chart_x, chart_y, self.chart['pie_width'], self.chart['pie_height'], mask='auto')
        return self

    def draw_nondac(self):
        # location
        x_offset = 350
        y_offset = 490
        title_x = x_offset + self.chart['pie_title_x_offset']
        title_y = y_offset + self.chart['pie_title_y_offset']
        chart_x = x_offset
        chart_y = y_offset

        if self.debug:
            self.c.rect(x_offset, y_offset, 200, 200)

        # draw title
        title = 'Top 5 NonDAC Development Partners'
        p = Paragraph(title, getSampleStyleSheet()['Normal'])
        p.wrapOn(self.c, 100, 100)
        p.drawOn(self.c, title_x, title_y)

        chart = 'charts/pie_chart_' + self.rec + '_nondac.png'
        self.c.drawImage(chart, chart_x, chart_y, self.chart['pie_width'], self.chart['pie_height'], mask='auto')
        return self

    def draw_multi(self):
        # location
        x_offset = self.PAGEWIDTH / 2 - 100
        y_offset = 350
        title_x = x_offset + self.chart['pie_title_x_offset']
        title_y = y_offset + self.chart['pie_title_y_offset']
        chart_x = x_offset
        chart_y = y_offset

        if self.debug:
            self.c.rect(x_offset, y_offset, 200, 200)

        # draw title
        title = 'Top 5 MultiLateral Development Partners'
        p = Paragraph(title, getSampleStyleSheet()['Normal'])
        p.wrapOn(self.c, 100, 100)
        p.drawOn(self.c, title_x, title_y)

        # draw chart
        chart = 'charts/pie_chart_' + self.rec + '_multi.png'
        self.c.drawImage(chart, chart_x, chart_y, self.chart['pie_width'], self.chart['pie_height'], mask='auto')
        return self

    def draw_bars(self):
        border = 40
        height = 300
        width = self.PAGEWIDTH - border * 2
        x_offset = border
        y_offset = self.PAGEHEIGHT - 750
        chart_x = x_offset
        chart_y = y_offset

        if self.debug:
            self.c.rect(x_offset, y_offset, width, height)

        return self

    def draw_agenda(self):
        self.c.showPage()

        x_offset = self.PAGEWIDTH /2 - 100
        y_offset = 600

        if self.debug:
            self.c.rect(x_offset, y_offset, 200, 160)

        return self

    def draw_usefulness(self):
        x_offset = 100
        y_offset = 400

        if self.debug:
            self.c.rect(x_offset, y_offset, 200, 160)

        return self

    def draw_helpfulness(self):
        x_offset = 300
        y_offset = 400

        if self.debug:
            self.c.rect(x_offset, y_offset, 200, 160)

        return self

    def draw_avg_influence(self):
        border_x = 100
        width = self.PAGEWIDTH - border_x * 2
        x_offset = border_x
        y_offset = 20

        if self.debug:
            self.c.rect(x_offset, y_offset, width, 330)

        return self

    def draw_footer(self):
        logo = ImageReader('assets/images/aiddata_main_wht.png')
        x_offset = 0
        y_offset = 0
        width = self.PAGEWIDTH
        height = 70

        self.c.setFillColorRGB(.086, .121, .203)
        self.c.rect(x_offset, y_offset, width, height, fill=1)

        logo_x = x_offset + 450
        logo_y = y_offset
        self.c.drawImage(logo, logo_x, logo_y, 120, 68, preserveAspectRatio=True, mask='auto')
        return self

    def save(self):
        self.c.save()
        return self

if __name__ == '__main__':
    for rec in ['Afghanistan']:
        p = RecipientProfile(rec)
        p.save()
