# Copy code from earlier version.


@gin.configurable
class Evaluator(object):
    def __init__(self):
        pass
    def eval():
        pass

def main(model, data_reader, args):
    # read in test data
    # forward pass with model
    # display metrics, save results
    pass

def single_move():
    #TODO
    pass

if __name__ == "__main__":
    args = parse_args.parse()
    data_reader = create_data.main(args)
    model = train.main(data_reader, args)
    main(model, data_reader, args)
