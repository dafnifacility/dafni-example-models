function helloWorld()
    % Get parameter called PARAMETER
    value = getenv('PARAMETER');
    disp(value)
    % Convert parameter to numeric value
    parameter = str2double(value);
    
    % Get input matrix
    input = readmatrix('dataset.csv');
    disp(input)
    
    % Use parameter value
    output = input + parameter;
    % Display result of function
    disp(output)
    
    % Write output to file
    writematrix(output, 'output.txt');
    % Display content of file
    type output.txt
end
