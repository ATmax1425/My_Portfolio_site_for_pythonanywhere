import base64
from io import BytesIO
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from django.shortcuts import render, redirect


matplotlib.use('Agg')


def plot_chart(data, chart, **kwargs):
    plt.figure(figsize=(10, 4), dpi=100)
    plt.xticks(rotation=45)

    if chart == "scatter":
        sns_plot = sns.scatterplot(data=data, x=kwargs["x_value"], y=kwargs["y_value"], hue=kwargs["hue"],
                                   palette=kwargs["palette"], style=kwargs["style"], size=kwargs["size"],
                                   sizes=kwargs["sizes"])
    elif chart == "line":
        sns_plot = sns.lineplot(data=data, x=kwargs["x_value"], y=kwargs["y_value"], hue=kwargs["hue"],
                                palette=kwargs["palette"], style=kwargs["style"], size=kwargs["size"],
                                sizes=kwargs["sizes"])
    elif chart == "histogram":
        sns_plot = sns.histplot(data=data, x=kwargs["x_value"], y=kwargs["y_value"], hue=kwargs["hue"],
                                multiple=kwargs["multiple"], bins=kwargs["bins"], shrink=kwargs["shrink"],
                                fill=kwargs["fill"], kde=kwargs["kde"])
    elif chart == "kde":
        sns_plot = sns.kdeplot(data=data, x=kwargs["x_value"], y=kwargs["y_value"], hue=kwargs["hue"],
                               fill=kwargs["fill"])
    elif chart == "ecd":
        sns_plot = sns.ecdfplot(data=data, x=kwargs["x_value"], hue=kwargs["hue"], stat=kwargs["stat"])
    elif chart == "bar":
        sns_plot = sns.barplot(data=data, x=kwargs["x_value"], y=kwargs["y_value"], hue=kwargs["hue"],
                               palette=kwargs["palette"])
    else:
        sns_plot = sns.countplot(data=data, x=kwargs["x_value"], hue=kwargs["hue"], palette=kwargs["palette"])
    if chart not in ["histogram", "kde", "ecd", "bar"]:
        sns_plot.legend(loc='upper left', bbox_to_anchor=(1, 1))
    sns_plot.figure.savefig("output.png")
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf8')


# Create your views here.
def home(request):
    return render(request, 'main_app/home.html')


def visualizer(request, data):
    response = render(request, 'main_app/visualizer.html')
    response.set_cookie("sample_data", data)
    return response


def get_data(request):
    sample_data = request.COOKIES.get('sample_data')
    if not sample_data:
        return redirect("home")
    else:
        data = sns.load_dataset(sample_data).round(2)
    return data


def show_data(request):
    data = get_data(request)
    columns = data.columns
    all_values = enumerate(data.values)
    return render(request, 'main_app/show_data.html', {"columns": columns, "all_values": all_values})


def relational_chart(request, chart):
    data = get_data(request)
    attributes = list(data.columns)
    plot_url = None
    min_max = [i for i in range(1, 21)]
    if request.method == 'POST':
        x_value = request.POST.get("x_axis")
        y_value = request.POST.get('y_axis')
        hue = request.POST.get('hue')
        palette = request.POST.get('palette')
        style = request.POST.get('style')
        size = request.POST.get('size')
        min_size = request.POST.get('min_size')
        max_size = request.POST.get('max_size')
        sizes = (min_size, max_size)

        if hue == "None":
            hue = None
            palette = None
        if palette == "default":
            palette = None
        if style == "None":
            style = None
        if size == "None":
            size = None
            sizes = None
        elif sizes[0] == "None" or sizes[1] == "None":
            sizes = None
        else:
            sizes = tuple([int(i) * 10 for i in sizes])
        plot_url = plot_chart(data=data, chart=chart, x_value=x_value, y_value=y_value, hue=hue, palette=palette,
                              style=style, size=size, sizes=sizes)
    return render(request, 'main_app/relational_chart.html',
                  {"chart": chart, "attributes": attributes, "plot_url": plot_url, "min_max": min_max})


def distribution_chart(request, chart):
    data = get_data(request)
    attributes = list(data.columns)
    plot_url = None
    shrink_in = [i for i in range(9, 4, -1)]

    if chart == "histogram":
        required = ['x_value', 'y_value', 'hue', 'multiple', 'bins', 'shrink', 'fill', 'kde']
    elif chart == "kde":
        required = ['x_value', 'y_value', 'hue', 'fill']
    else:
        required = ['x_value', 'hue', 'stat']

    if request.method == 'POST':
        required_att = {req: request.POST.get(req) for req in required}
        if chart == "histogram":
            in_ = required_att["bins"]
            required_att["bins"] = abs(round(float(in_))) if in_ != "" else "auto"
            shrink_ = required_att["shrink"]
            required_att["shrink"] = int(shrink_) / 10
            required_att["kde"] = True if required_att["kde"] else False
        if "fill" in required:
            required_att["fill"] = True if required_att["fill"] else False
        if "y_value" in required:
            y_value_ = required_att["y_value"]
            required_att["y_value"] = y_value_ if y_value_ != "None" else None
        hue_ = required_att["hue"]
        required_att["hue"] = hue_ if hue_ != "None" else None

        print(required_att)
        plot_url = plot_chart(data=data, chart=chart, **required_att)
    return render(request, 'main_app/distribution_chart.html',
                  {"chart": chart, "attributes": attributes, "plot_url": plot_url, "required": required,
                   "shrink_in": shrink_in})


def categorical_chart(request, chart):
    data = get_data(request)
    attributes = list(data.columns)
    plot_url = None

    if chart == "bar":
        required = ['x_value', 'y_value', 'hue', 'palette']
    else:
        required = ['x_value', 'hue', 'palette']

    if request.method == 'POST':
        required_att = {req: request.POST.get(req) for req in required}
        if "y_value" in required:
            y_value_ = required_att["y_value"]
            required_att["y_value"] = y_value_ if y_value_ != "None" else None
        if required_att["palette"] == "default":
            required_att["palette"] = None
        if required_att["hue"] == "None":
            required_att["hue"] = None
        plot_url = plot_chart(data=data, chart=chart, **required_att)

    return render(request, 'main_app/categorical_chart.html',
                  {"chart": chart, "attributes": attributes, "plot_url": plot_url, "required": required})
