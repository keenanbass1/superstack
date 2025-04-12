interface ReviewOptions {
    model: string;
    context: boolean;
}
export declare function review(filePath: string, options: ReviewOptions): Promise<void>;
export {};
