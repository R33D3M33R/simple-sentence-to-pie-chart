#!/usr/bin/env python
from __future__ import division
import math

__author__ = "Andrej Mernik"
__copyright__ = "Copyright 2015 Andrej Mernik"
__license__ = "GPLv3"

'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


class SimpleSentenceToPieChart:
    ''' Visually represent a short sentence as a PieChart '''
    def __init__(self, sentence):
        self.stats = {}
        self.coords = {}
        self.letters = 0

        self.ignored_letters = set([' ', '\t'])    # ignore spaces or tabs
        self.colors = ['LightBlue', 'SteelBlue', 'LightGreen', 'ForestGreen', 'Salmon', 'FireBrick', 'NavajoWhite', 'DarkOrange', 'Violet', 'Purple']    # some sample colors, if you want more PieChart items, just add more colors to the list

        self.radius = 150    # radius of the PieChart
        self.center = {'x': 200, 'y': 200}    # the center point of the PieChart
        self.line = {'x': self.radius, 'y': 0}    # the first line of the PieChart will be drawn from center to this point

        self.sentence = sentence.lower()    # don't differentiate between upper and lower case

        try:
            self.analyze()
            if len(self.stats) == 0:
                raise SystemExit('Empty string')
            elif len(self.stats) > len(self.colors):
                raise SystemExit('Input has too many different letters. Use maximum of ' + str(len(self.colors)) + ' letters or add more colors to the colors list.')
            else:
                # everything is ok so prepare the PieChart data for later drawing
                self.prepare()
        except Exception as e:
            print('An exception has occurred. ' + e.message)

    def analyze(self):
        ''' count number of different letters in the given sentence '''
        for letter in self.sentence:
            if letter not in self.ignored_letters:
                self.letters += 1
                if letter not in self.stats:
                    self.stats[letter] = 1
                else:
                    self.stats[letter] += 1

    def prepare(self):
        ''' calculate coordinates for the circular sectors '''
        angle_total = 0
        for letter, amount in self.stats.iteritems():
            angle = amount/self.letters * 360    # the angle in degrees
            angle_total += angle    # total angle in degrees
            angle_total_radians = math.radians(angle_total)    # convert to radians for trigonometry calculations

            # convert angles to coordinates
            arcx = int(math.cos(angle_total_radians) * self.radius)
            arcy = int(math.sin(angle_total_radians) * self.radius)

            self.coords[letter] = {'linex': self.line['x'], 'liney': self.line['y'], 'arcx': arcx, 'arcy': arcy, 'widearc': 1 if angle > 180 else 0}
            self.line['x'] = arcx
            self.line['y'] = arcy

    def draw(self):
        ''' output the PieChart as SVG '''
        output = '<svg width="' + str(self.center['x']*2 + 100) + '" height="' + str(self.center['y']*2 + 100) + '">\n'
        legend = 25
        if len(self.coords) > 1:
            for index, letter in enumerate(self.coords):
                output += '<path d="M ' + str(self.center['x']) + ',' + str(self.center['y']) + ' l ' + str(self.coords[letter]['linex']) + ',' + str(-self.coords[letter]['liney']) + ' a' + str(self.radius) + ',' + str(self.radius) + ' 0 ' + str(self.coords[letter]['widearc']) + ',0 ' + str(self.coords[letter]['arcx']-self.coords[letter]['linex']) + ',' + str(-(self.coords[letter]['arcy']-self.coords[letter]['liney'])) + ' z" fill="' + self.colors[index] + '" />\n'
                output += '<rect x="' + str(self.center['x']*2) + '" y="' + str(legend) + '" width="30" height="30" fill="' + self.colors[index] + '" stroke="black" stroke-width="1" />\n'
                output += '<text x="' + str(self.center['x']*2 + 40) + '" y="' + str(legend + 20) + '">' + letter + '</text>\n'
                legend = legend + 35
        else:
            output += '<circle cx="' + str(self.center['x']) + '" cy="' + str(self.center['y']) + '" r="' + str(self.radius) + '" fill="' + self.colors[0] + '" stroke="black" stroke-width="1" />\n'
            output += '<rect x="' + str(self.center['x']*2) + '" y="' + str(legend) + '" width="30" height="30" fill="' + self.colors[0] + '" stroke="black" stroke-width="1" />\n'
            output += '<text x="' + str(self.center['x']*2 + 40) + '" y="' + str(legend + 20) + '">' + str(self.coords.keys()[0]) + '</text>\n'

        output += '</svg>\n'
        return output

    def __str__(self):
        return self.draw()

if __name__ == "__main__":
        string = 'Hello World!'
        name = 'Simple Sentence to PieChart Demo: ' + string

        f = open('simple-sentence-to-pie-chart-demo.html', 'w')
        f.write('<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8" />\n<title>' + name + '</title>\n</head>\n<body> \n<h1>' + name + '</h1>\n')
        f.write(str(SimpleSentenceToPieChart(string)))
        f.write('</body>\n</html>')
