interface GenerateOptions {
    description?: string;
    model: string;
    context: boolean;
}
export declare function generate(type: string, options: GenerateOptions): Promise<void>;
export {};
