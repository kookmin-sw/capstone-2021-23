#-*- encoding: utf-8 -*-. -

f = open("template2.html")
data = f.read()
f.close()

start = data.find("<findme_start>")
end = data.find("<findme_end>")

new_str = data[start:end+12].format(space="국민대학교 미래관 609호")

print(data[:start] + new_str + data[end+12:])

print(start)
print(end)
