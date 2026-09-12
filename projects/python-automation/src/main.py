from file_organizer import organize_files


def main() -> None:
	input_directory = "data/input"
	output_directory = "data/output"

	print("Starting file organization...")
	organize_files(input_directory, output_directory)
	print("File organization completed.")


if __name__ == "__main__":
	main()
