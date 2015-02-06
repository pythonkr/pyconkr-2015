var values = {
    friction: 0.1,
    timeStep: 0.01,
    amount: 6
};

var path;

var sinPath;
var boxPath;
var mask;

var tilt = 0;
var iOS = false;

function isiOS()
{
    return (navigator.userAgent.match(/(iPad|iPhone|iPod)/i) != null);
}

function createPath() {
    if (sinPath) sinPath.remove();
    if (boxPath) boxPath.remove();
    if (mask) mask.remove();
    if (path) path.remove();

    sinPath = new Path();
    boxPath = new Path([
        new Point(0.0, 0.5) * size,
        new Point(0.0, 1.0) * size,
        new Point(1.0, 1.0) * size,
        new Point(1.0, 0.5) * size
    ]);

    for (var i = 0; i <= values.amount; i++) {
        var segment = sinPath.add(
            new Point(i / values.amount, 0.5) * size
        );
        var point = segment.point;
        point.fixed = i < 1 || i > values.amount - 1;
        point.i = i;
        point.vy = 0;
        point.ty = 0.5;
    }

    path = new CompoundPath({
        children: [
            sinPath,
            boxPath
        ],
        fillColor: {
            gradient: {
                stops: [
                    '#ffe873',
                    '#ffd43b'
                ]
            },
            origin: boxPath.bounds.topLeft,
            destination: boxPath.bounds.bottomRight
        }
    });

    mask = new CompoundPath({
        children: [
            new Path.Circle(new Point(0.5, 0.5) * size, size.width * 0.45),
            new Path.Rectangle(new Point(0,0), new Point(1,1) * size)
        ],
        fillColor: '#ffffff'
    });
}

function onResize() {
    size =  new Size(640, 640);
    view.viewSize = size;
    createPath();
}

function onFrame(event) {
    updateWave(sinPath);

    var t = tilt / 35.0;
    for (var i = 0; i <= values.amount; i++) {
        var point = sinPath.segments[i].point;
        point.ty = (Math.sin(point.i*Math.PI/values.amount*2)*0.15+0.5+(t * (values.amount/2-point.i))) * size.height;
    }
}

function updateWave(path) {
    var force = (1 - values.friction) * values.timeStep;

    for (var i = 1, l = path.segments.length - 1; i < l; i++) {
        var point = path.segments[i].point;
        point.vy += (point.ty - point.y) * force;
        point.vy *= 0.95;

        var previous_point = path.segments[i - 1].point;
        point.vy -= previous_point.vy * 0.1;

        var next_point = path.segments[i + 1].point;
        point.vy += next_point.vy * 0.1;

        point.y = Math.max(point.y + point.vy, 0);
    }
    path.smooth();
}

function onMouseMove(event) {
    var location = sinPath.getNearestLocation(event.point);
    var segment = location.segment;
    var point = segment.point;

    if (!point.fixed && location.distance < size.height / 4) {
        var y = event.point.y;
        point.vy += (y - point.y) / 6 * values.friction;
        if (segment.previous && !segment.previous.point.fixed) {
            var previous = segment.previous.point;
            previous.vy += (y - previous.y) / 24 * values.friction;
        }
        if (segment.next && !segment.next.point.fixed) {
            var next = segment.next.point;
            next.vy += (y - next.y) / 24 * values.friction;
        }
    }
}

function onKeyDown(event) {
    if (event.key == 'space') {
        path.fullySelected = !path.fullySelected;
    } else if (event.key == 'a') {
        tilt = -10;
    } else if (event.key == 'b') {
        tilt = 0;
    } else if (event.key == 'c') {
        tilt = 10;
    }
}

$(function() {
    iOS = isiOS();
    window.ondevicemotion = function(event) {
        if( iOS )
        {
            tilt = event.accelerationIncludingGravity.x;
        }
        else
        {
            tilt = -event.accelerationIncludingGravity.x;
        }
    }
});
