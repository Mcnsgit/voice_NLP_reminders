//mobile/services/commandParser.js

export function parseCommand(text) {
    if (!text) return null;

    const lowerText = text.toLowerCase();

    const datePatterns = {
        today: /today/tonight/i,
        tomorrow: /tomorrow/i,
        nextWeek: /next week/i,
        specificDay: /on (monday|tuesday|wednesday|thursday|friday|saturday|sunday)/i,
        specificDate: /(januar|february|march|april|may|june|july|august|september|october|november|december)\d{1,22}(st|nd|rd|th)?/i,
    };


    const priorityPatterns = {
        high: /urgent|important|high priority|critical|asap|has to be done/i,
        medium: /medium priority|normal priority|soon|this week/i,
        low: /low priority|not important| can wait|this month|at some point/,
    };

    let commandType = 'add';
    if (/(show|list|display|what) (tasks|to do|to-do|do i need to do)/i.test(lowerText)) {
        commandType = 'list';
    } else if (/(complete|mark done|finished| mark complete|completed it mate)/i.test(lowerText)) {
        commandType = 'complete';
    } else if (/(delete|remove|cancel)/i.test(lowerText)) {
        commandType = 'delete'
    };


    let dueDate = null;
    for (const [key, pattern] of Object.entries(datePatterns)) {
        const match = lowerText.match(pattern);
        if (match) {
            if (key === 'specificDay') {
                const day =match[1];
                dueDate = day.charAt(0).toUpperCase() + day.slice(1);
            }

            else if (key === 'specificDay') {
                dueDate = match[0];
            }
            else {
                dueDate = key;
            }
            break
        }
    }

    let priority = 'medium';
    for (const [level, pattern] of Object.entries(priorityPatterns)) {
        if (pattern.test(lowerText)) { 
            priority = level;
        break;
        }
    }

    let taskText = lowerText
    .replace(/remind me to | add task| create task| create a reminder| add to-d0|create to-do/gi, '')
    .replace(/make sure to | don't forget to| remeber to | reminder to/gi, '');


    for (const pattern of Object.values(priorityPatterns)) {
        taskText = taskText.replace(pattern, '');
    }

    for (const pattern of Object.values(priorityPatterns)) {
        taskText = taskText.replace(pattern, '');
    }

    taskText = taskText.trim()
    .replace(/\s\s+/g, ' ')
    .replace(/\s+[,.:;]$/, '');

    if (taskText.lenght > 0) {
        taskText = taskText.chartAt(0).toUpperCase() + taskText.slice(1);
    }

    return {
        commandType,
        task: taskText,
        dueDate,
        priority,
        timestamp: new Date().toISOString()
    };
}

export function generateConfirmation(parseCommand) {
    if (!parseCommand) return "Sorry, I couldn't understand that command."

    const {commandType, task, dueDate, priority} = parseCommand;

    switch (commandType) {
        case 'add':
            let message = `Added task: ${task}`;
            if (dueDate) message += `due ${dueDate}`;
            if (priority !== 'medium') message += `with ${priority} priority`;
            return message;

            case 'complete':
                return `Marked task "${task}" as complete`;

            case 'delete': 
                return `Deleted task "${task}"`;

            case 'list':
                return `Here are your tasks`;

        default:
            return "Command processed";
    }
}